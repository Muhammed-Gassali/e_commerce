from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import products,category,Order,OrderItem,ShippingAddress,ProfilePicture   
from django.http import JsonResponse
import json
import datetime
import uuid

# importing image cropping
import base64
from django.core.files.base import ContentFile

# importiing razorpay
import razorpay
from django.views.decorators.csrf import csrf_exempt



from  django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File


# Create your views here.

# function used to admin login
def adminlogin(request):
    if request.session.has_key('adminusername'):
        return redirect(admindashboard)
    if request.method == "POST":
        adminusername = request.POST['username']
        adminpassword = request.POST['password']
        if adminusername == "admin" and adminpassword == "5554":
            request.session['adminusername']= adminusername
            return  render(request, 'admindashboard.html')
            # return HttpResponse("hai")
        else:
             messages.info(request, 'invalid credentials')
             return render(request, 'adminlogin.html')
    else:
        return render(request, 'adminlogin.html')
    # else:
    #      return render(request, 'adminlogin.html')

# function for admin logout
def adminlogout(request):
    if request.session.has_key('adminusername'):
        request.session.flush()
        return redirect(adminlogin)
    else:
        return render(request, 'admindashboard.html')



# function used to load admin dashboard
def admindashboard(request):
    if request.session.has_key('adminusername'):
        return render(request, 'admindashboard.html')
    else:
        return redirect(adminlogin)

# function used to manage product management
def productmanagement(request):
    if request.session.has_key('adminusername'):
        product = products.objects.all().order_by('id')
        return render(request, 'adminhomepage.html', {'product':product})
    else:
        return redirect(adminlogin)

    

# function used to add products by admin
def addproduct(request):
    if request.session.has_key('adminusername'):
        if request.method == 'POST':
            productname = request.POST['product_name']
            cat = category.objects.get(category_name=request.POST['category'])
            price = request.POST['price']
            image = request.FILES.get('image')
            desc = request.POST['desc']
            quantity = request.POST['quantity']

            # image cropping 
            image_data = request.POST['pro_img']

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name=productname + '.' + ext)

            product = products.objects.create(product_name=productname, category=cat, price=price, description=desc, image=data, quantity=quantity)
            product.save()
            return redirect(productmanagement)
        else:
            # return HttpResponse("keriyill")
            return render(request, 'addproductdetials.html')
    else:
        return redirect(adminlogin)


# function used to delete product by admin
def delete(request,id):
    if request.session.has_key('adminusername'):
        b = products.objects.get(id = id)
        print(id)
        b.delete()
        messages.info(request, 'deleted successfully')
        return redirect(productmanagement)
    else:
        return redirect(adminlogin)


# function used to load edit  product page 
def edit(request, id):
    if request.session.has_key('adminusername'):
        value=products.objects.get(id=id)
        return render(request, 'editproduct.html', {'values':value})
    else:
        return redirect(adminlogin)
 




        




# function used to update product by admin
def update(request,id):
    if request.session.has_key('adminusername'):
        if request.method == 'POST':
            productname = request.POST['product_name']
            category = request.POST['category']
            price = request.POST['price']
            # image = request.FILES.get('image')
            desc = request.POST['desc']
            quantity = request.POST['quantity']
            value = products.objects.get(id=id)
            value.product_name = productname
            value.category.category_name = category
            value.price = price
            
            value.description = desc

            if 'image' not in request.POST:
                image = request.FILES.get('image')
            else:
                image = value.image
            value.image = image



            value.quantity = quantity
            value.save()
            return redirect(productmanagement)
        else:
            return render(request, 'editproduct.html')
    else:
         return redirect(adminlogin)


# function used to load user management page
def usermanagemnet(request):
    if request.session.has_key('adminusername'):
        user = User.objects.all().order_by('id')
        return render(request, 'usermanagemnet.html', {'user':user})
    else:
        return redirect(adminlogin)
    
#function for delete user by admin
def deleteuser(request, id):
    if request.session.has_key('adminusername'):
        b = User.objects.get(id = id)
        b.delete()
        messages.info(request, 'deleted successfully')
        return redirect(usermanagemnet)
    else:
        return redirect(adminlogin)


# function for lod  edit user page
def edituser(request, id):
    if request.session.has_key('adminusername'):
        value=User.objects.get(id=id)
        return render(request, 'edituser.html', {'values':value})
    else:
        return redirect(adminlogin)


# function for update user by admin
def updateuser(request, id):
    if request.session.has_key('adminusername'):
        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
            value = User.objects.get(id=id)
            value.first_name = name
            value.username = username
            value.email = email
            value.last_name = mobile
            value.save()
            return redirect(usermanagemnet)
        else:
            return render(request, 'edituser.html')
    else:
         return redirect(adminlogin)




# function for adding user by admin

def adduser(request):
    if request.session.has_key('adminusername'):
        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password = request.POST['password1']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'username already exists')
                        return render(request, 'useradd.html')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'email already exists')
                        return render(request, 'useradd.html')
                else:
                    user = User.objects.create_user(first_name=name, username=username, email=email, password=password, last_name=mobile)
                    user.save()
                    return redirect('usermanagemnet')
            else:
                messages.info(request, 'password does not match')
                return render(request, 'useradd.html')
        else:
            return render(request, 'useradd.html')
    else:
        return redirect(adminlogin)


#category management by admin
def categorymanagement(request):
    value = category.objects.all().order_by('id')
    return render(request, 'categorymanagement.html', {'value':value})


#add catogory
def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        value = category.objects.create(category_name=category_name)
        value.save()
        return redirect(categorymanagement)
    else:
        return render(request, 'addcategory.html')

#function for delete category
def deletecategory(request, id):
        b = category.objects.get(id=id)
        b.delete()
        messages.info(request, 'deleted successfully')
        return redirect(categorymanagement)


def manage_order(request):
    if request.session.has_key('adminusername'):
        table = Order.objects.all()
        return render(request, 'orderadminview.html', {'table_data': table})
    else:
        return redirect(adminlogin)


def delete_order(request, id):
    if request.session.has_key('adminusername'):
        b = Order.objects.get(id = id)
        b.delete()
        messages.info(request, 'deleted successfully')
        return redirect(manage_order)
    else:
        return redirect(adminlogin)



# user side --------------------------------------------------------------------------------------------user side


# fuction used for loading userlogin
def userlogin(request):
    if request.user.is_authenticated:
        return redirect('registereduserhomepage')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
            
            
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
                # return JsonResponse("hai", safe=False)
            value = products.objects.all()
            return redirect('registereduserhomepage')
        else:
            
            value={"username":username}
            messages.info(request, 'invalid credentials')
                # return JsonResponse('hooi', safe=False)
            return redirect('userlogin')
                # return render('home.html', {"values":value})

            
            # return render(request, 'home.html')
    else:
        return render(request, 'userloginpage.html')
    

#function for loading userhome page
# def userhome(request):
#     if request.user.is_authenticated:
#         return render(request, 'userhome.html') 
    # else:
    #     return redirect('/')


# function for user logout
def userlogout(request):
    if request.user.is_authenticated:
       auth.logout(request)
       return redirect('/')
   




# function used to userregistrtaion
def userregistration(request):
    if request.user.is_authenticated:
        return redirect('registereduserhomepage')

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'username already exists')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already exists')
                return render(request, 'userregistration.html')
            else:
                user = User.objects.create_user(first_name=name, username=username, email=email, password=password, last_name=mobile)
                user.save()
                return redirect('userlogin')
        else:
            messages.info(request, 'Password does not matching')
            return render(request, 'userregistration.html')
        

    else:      
        return render(request, 'userregistration.html')





# function to test user hom page
def userhomepage(request):
    if request.user.is_authenticated:
        return redirect(registereduserhomepage)
    else:
        value= products.objects.all()
        return render(request, 'userhomepagenew/index.html',{'value':value})
        


#function to get registered user home page
def registereduserhomepage(request):
    if request.user.is_authenticated:
        value= products.objects.all()
        user = request.user
        print("entered")
        print(user)
        return render(request, 'userhomepagenew/registereduser.html',{'value':value, 'user':user})
    else:
        return redirect(userlogin)

def contact(request):
    return render(request, 'userhomepagenew/contact.html')

def quickview(request, id):
    print(id)
    product = products.objects.filter(id=id).first()
    return render(request, 'userhomepagenew/single.html', {'product': product})


# def checkout(request):
   
#     if request.method == 'POST':
#         return render(request, 'userhomepagenew/checkout.html')
#     else:
#         return render(request, 'userhomepagenew/checkout.html')


def cart(request):
    print("--------------------------------Entered cart function---------------------------------")
    if request.user.is_authenticated:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        total_price = 0
        for x in cart:
            total_price = total_price + x.get_total

        return render(request, 'userhomepagenew/cart.html', {'cart_data': cart, 'total_price':total_price})
    else:
        return render(request, 'userhomepagenew/index.html')


def add_cart(request, id):
    print("----------------------------------entered add_cart function--------------------------")
    if request.user.is_authenticated:
        user = request.user
        product = products.objects.get(id=id)
        if OrderItem.objects.filter(product=product).exists():
            order = OrderItem.objects.get(product=product)
            if order.quantity <= order.product.quantity:
                order.quantity = order.quantity+1
                order.save()
                return redirect(cart)
            else:
                return redirect(registereduserhomepage)
        else:
            quantity = 1

            items = OrderItem.objects.create(user=user, product=product, quantity=quantity, total_price=product.price*quantity)
            return redirect(cart)
        
    else:
        return render(request, 'userhomepagenew/index.html')


def user_removeOrderItem(request, id):
    b = OrderItem.objects.get(id=id)
    b.delete()
    print("Deleted Order")
    return redirect(cart)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        
        items = OrderItem.objects.filter(user=user)
        order = Order.objects.filter(user=user)
        
        total_price = 0
        for x in items  :
            total_price = total_price + x.get_total

        # razorpay integrate
        if request.method == "POST":
            amount = total_price*100*70
            print("enterd ######################################")
            print(amount)
            order_currency = 'INR'
            client = razorpay.Client('Uci1HLeyYAs4mMBvKzysJL2X', auth='rzp_test_666QJpopWh4z27')
            payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})

        return render(request, 'userhomepagenew/checkout.html', {'items': items, 'order': order, 'total_price':total_price, 'user':user})
    else:
        return render(request, 'userhomepagenew/index.html')


def user_payment(request):
    print("Entered user paymnet function ----------------------------")
    if request.user.is_authenticated:
        print("Authenticated User")
        if request.method == 'POST':
            print("post")
            user = request.user
            address = request.POST['address1']
            state = request.POST['state']
            city = request.POST['city']
            zipcode = request.POST['zipcode']
            address = ShippingAddress.objects.create(user=user, address=address, state=state, city=city, zipcode=zipcode)

            cart = OrderItem.objects.filter(user=user)
            date = datetime.datetime.now()
            transaction_id = uuid.uuid4()
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product,
                                     total_price=item.product.price,
                                     transaction_id=transaction_id, date_ordered=date, complete=True)
                item.product.save()
            cart.delete()
            messages.info(request, "Placed Order")
            return redirect(registereduserhomepage)
            # return render(request, 'home/payment.html')
        else:
            print("entered payment else conditioin")
            return render(request, 'userhomepagenew/checkout.html')
    else:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'userhomepagenew/checkout.html')



def user_order(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user)
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'userhomepagenew/user_order.html', {'item_data': order})
    return render(request, 'userhomepagenew/user_order.html')



def profile(request):
    if request.user.is_authenticated:
        user = request.user
        if ProfilePicture.objects.filter(user=user).exists():
            img=ProfilePicture.objects.get(user=user)
        print(img.ImageURL)
        return render(request, 'userhomepagenew/userprofile.html', {'value':user, 'img':img})
    else:
        return redirect(userhomepage)


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print("enterered  #######################################")
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
        
            value = request.user
            value.first_name = name
            value.username = username
            value.email = email
            value.last_name = mobile
            value.save() 
            image = request.FILES.get('image')
            user=request.user
            if ProfilePicture.objects.filter(user=user).exists():
                img = ProfilePicture.objects.get(user=user)
                if image is not None:
                    img.image = image
                    img.save()
            else:
                if image is not None:
                    img = ProfilePicture.objects.create(image=image, user=user)
                
            
            
            return redirect('profile')
        else:
            return redirect('userhomepage')
    else:
        return redirect(userhomepage)






# def quickview(request):
#     return render(request, 'userhomepagenew/single.html')


# def contact(request):
#     return render(request, 'userhomepagenew/contact.html')

# def product(request):
#     return render(request, 'userhomepagenew/product.html')










# def registereduser(request):
#     value = products.objects.all()
#     print(value)
#     return render(request, 'userhomepagenew/registereduser.html',{'value':value})



# def nw_userhome(request):
#     if request.user.is_authenticated:
#         value = products.objects.all()
#         return render(request, 'nw/store.html', {"value":value})
#         # user = request.user
#         # value=products.objects.all()
#         # order, created = Order.objects.get_or_create(user=user, complete=False)
#         # items = order.orderitem_set.all()
#         # print("hello ", items)
#         # cartitems = order.get_cart_items
#         # context = {'value':value, 'cartitems':cartitems}
#         # return render(request, 'nw/store.html', context)
#     else:
#         return redirect(actual_userhome)

# def actual_userhome(request):
#     if request.user.is_authenticated:
#         return redirect(nw_userhome)
#     else:
#         value=products.objects.all()
#         return render(request, 'nw/actualuserhome.html',  {"value":value})


# functio for adding to cart
# def updateitem(request):

#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']

#     print(action)
#     print(productId)
    
#     user = request.user
#     print(user)
#     product = products.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(user=user, complete=False)
#     print(product)

#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)
    
#     orderItem.save()

#     if orderItem.quantity <= 0:
#         orderItem.delete()
#     return JsonResponse('item was Added', safe=False)

# def cart(request):
#     if request.user.is_authenticated:
#         user = request.user
#         order, created = Order.objects.get_or_create(user=user, complete=False)
#         items = order.orderitem_set.all()
#         print("hello ", items)
#         cartitems = order.get_cart_items
#     else:
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0}
#         cartitems = order['get_cart_items']
#     context = {'items':items,'order':order, 'cartitems':cartitems, }
#     return render(request, 'nw/cart.html', context)

# def checkout(request):
#     if request.user.is_authenticated:
#         user = request.user
#         order, created = Order.objects.get_or_create(user=user, complete=False)
#         items = order.orderitem_set.all()
#         print("hello ", items)
#         cartitems = order.get_cart_items
#     else:
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0}
#         cartitems = order['get_cart_items']
#     context = {'items':items,'order':order, 'cartitems':cartitems, }
#     return render(request, 'nw/checkout.html', context)


# def processOrder(request):
#     transaction_id = datetime.datetime.now().timestamp()
#     data = json.loads(request.body)

#     if request.user.is_authenticated:
#         user = request.user
#         order, created = Order.objects.get_or_create(user=user, complete=False)
#         total = float(data['form']['total'])
#         order.transaction_id = transaction_id

#         if total == order.get_cart_total:
#             order.complete = True
#         order.save() 
#         ShippingAddress.objects.create(user=user,order=order,address=data['shipping']['address'],city=data['shipping']['city'],state=data['shipping']['state'],zipcode=data['shipping']['zipcode'])
        
#     else:
#         print('user not logged in')
#     return JsonResponse('Payment Complete', safe=False)


# def cart(request):
#     print("--------------------------------Entered cart function---------------------------------")
#     if request.user.is_authenticated:
#         user = request.user
#         cart = OrderItem.objects.filter(user=user)
#         return render(request, 'nw/cart.html', {'cart_data': cart})
#     else:
#         return render(request, 'nw/store.html')

    
    