from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import products,category,Order,OrderItem,ShippingAddress,ProfilePicture   
from django.http import JsonResponse
import json
import datetime 
from datetime import date
from django.db.models import Sum
import uuid

# importing image cropping
import base64
from django.core.files.base import ContentFile

# importiing OTP
import requests

import razorpay
 
from  django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File


# Create your views here.

# function used to admin login
def admin_login(request):
    if request.session.has_key('admin_username'):
        return redirect(admin_dashboard)
    if request.method == "POST":
        admin_username = request.POST['username']
        admin_password = request.POST['password']
        if admin_username == "admin" and admin_password == "5554":
            request.session['admin_username'] = admin_username
            return  render(request, 'admindashboard.html')
            # return HttpResponse("hai")
        else:
             messages.info(request, 'invalid credentials')
             return render(request, 'adminlogin.html')
    else:
        return render(request, 'adminlogin.html')



# function for admin logout
def admin_logout(request):
    if request.session.has_key('admin_username'):
        request.session.flush()
        return redirect(admin_login)
    else:
        return render(request, 'admindashboard.html')



# function used to load admin dashboard
def admin_dashboard(request):
    if request.session.has_key('admin_username'):
        users = User.objects.all().count()
        order = Order.objects.all().count()
        product = products.objects.all().count()
        context ={'users':users,'order':order, 'products':product}
        return render(request, 'admindashboard.html',context)
    else:
        return redirect(admin_login)

# function used to manage product management
def product_management(request):
    if request.session.has_key('admin_username'):
        product = products.objects.all().order_by('id')
        return render(request, 'adminhomepage.html', {'product':product})
    else:
        return redirect(admin_login)

    

# function used to add products by admin
def add_product(request):
    if request.session.has_key('admin_username'):
        if request.method == 'POST':
            product_name = request.POST['product_name']
            # cat = category.objects.get(category_name=request.POST['category'])
            cat = category.objects.get(id=request.POST['category'])
            price = request.POST['price']
            image = request.FILES.get('image')
            desc = request.POST['desc']
            quantity = request.POST['quantity']

            # image cropping 
            image_data = request.POST['pro_img']

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name=product_name + '.' + ext)

            product = products.objects.create(product_name=product_name, category=cat, price=price, description=desc, image=data, quantity=quantity)
            product.save()
            return redirect(product_management)
        else:
            value = category.objects.all()
            return render(request, 'addproductdetials.html', {'value':value})
    else:
        return redirect(admin_login)


# function used to delete product by admin
def delete(request,id):
    if request.session.has_key('admin_username'):
        value = products.objects.get(id = id)
        value.delete()
        messages.info(request, 'deleted successfully')
        return redirect(product_management)
    else:
        return redirect(admin_login)


# function used to load edit  product page 
def edit(request, id):
    if request.session.has_key('admin_username'):
        value = products.objects.get(id=id)
        return render(request, 'editproduct.html', {'values':value})
    else:
        return redirect(admin_login)
 



# function used to update product by admin
def update(request,id):
    if request.session.has_key('admin_username'):
        if request.method == 'POST':
            product = request.POST['product_name']
            category = request.POST['category']
            price = request.POST['price']
            # image = request.FILES.get('image')
            desc = request.POST['desc']
            quantity = request.POST['quantity']
            value = products.objects.get(id=id)
            value.product_name = product
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
            return redirect(product_management)
        else:
            return render(request, 'editproduct.html')
    else:
         return redirect(admin_login)


# function used to load user management page
def user_managemnet(request):
    if request.session.has_key('admin_username'):
        user = User.objects.all().order_by('id')
        return render(request, 'usermanagemnet.html', {'user':user})
    else:
        return redirect(admin_login)
    
#function for delete user by admin
def delete_user(request, id):
    if request.session.has_key('admin_username'):
        value = User.objects.get(id = id)
        value.delete()
        messages.info(request, 'deleted successfully')
        return redirect(user_managemnet)
    else:
        return redirect(admin_login)


def block_user(request, id):
    if request.session.has_key('admin_username'):
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect(user_managemnet)
    else:
        return redirect(admin_login)



# function for lod  edit user page
def edit_user(request, id):
    if request.session.has_key('admin_username'):
        value = User.objects.get(id=id)
        return render(request, 'edituser.html', {'values':value})
    else:
        return redirect(admin_login)


# function for update user by admin
def update_user(request, id):
    if request.session.has_key('admin_username'):
        if request.method == 'POST':
            name = request.POST['name']
            user_name = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
            value = User.objects.get(id=id)
            value.first_name = name
            value.username = user_name
            value.email = email
            value.last_name = mobile
            value.save()
            return redirect(user_managemnet)
        else:
            return render(request, 'edituser.html')
    else:
         return redirect(admin_login)




# function for adding user by admin

def add_user(request):
    if request.session.has_key('admin_username'):
        if request.method == 'POST':
            name = request.POST['name']
            user_name = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password = request.POST['password1']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
                    if User.objects.filter(username=user_name).exists():
                        messages.info(request, 'username already exists')
                        return render(request, 'useradd.html')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'email already exists')
                        return render(request, 'useradd.html')
                else:
                    user = User.objects.create_user(first_name=name, username=user_name, email=email, password=password, last_name=mobile)
                    user.save()
                    return redirect(user_managemnet)
            else:
                messages.info(request, 'password does not match')
                return render(request, 'useradd.html')
        else:
              
            return render(request, 'useradd.html')
    else:
        return redirect(admin_login)





#category management by admin
def category_management(request):
    value = category.objects.all().order_by('id')
    return render(request, 'categorymanagement.html', {'value':value})


#add catogory
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        value = category.objects.create(category_name=category_name)
        value.save()
        return redirect(category_management)
    else:
        return render(request, 'addcategory.html')

#function for delete category
def delete_category(request, id):
        b = category.objects.get(id=id)
        b.delete()
        messages.info(request, 'deleted successfully')
        return redirect(category_management)


def manage_order(request):
    if request.session.has_key('admin_username'):
        table = Order.objects.all()
        return render(request, 'orderadminview.html', {'table_data': table})
    else:
        return redirect(admin_login)


def delete_order(request, id):
    if request.session.has_key('admin_username'):
        b = Order.objects.get(id = id)
        b.delete()
        messages.info(request, 'deleted successfully')
        return redirect(manage_order)
    else:
        return redirect(admin_login)

def cancel_order(request, id):
    if request.session.has_key('admin_username'):
        b = Order.objects.get(id=id)
        if b.order_verify == True:
            b.order_verify = False
            b.save()
        else:
            b.order_verify = True
            b.save()
        return redirect(manage_order)
    else:
        return redirect(admin_login)

def report(request):
    
    if request.session.has_key('admin_username'):
        if request.method == "POST":
            
            start = request.POST['start_date']
            end = request.POST['end_date']
            success =  Order.objects.filter(date_ordered__range=[start, end], order_verify=True)
            fail =  Order.objects.filter(date_ordered__range=[start, end], order_verify=False)

            orders = Order.objects.filter(date_ordered__range=[start,end])
            dict = {}           
            for order in orders:
                if not order.transaction_id in dict.keys():
                    dict[order.transaction_id]=order
                    dict[order.transaction_id].orderprice = order.total_price
                    dict[order.transaction_id].total_products = 1
                else:
                    dict[order.transaction_id].orderprice += order.total_price
                    dict[order.transaction_id].total_products += 1
            order_success = {}
            order_cancelled = {}
            for x,y in dict.items():
                if y.order_verify == True:
                    if not y.date_ordered in order_success.keys():
                        order_success[y.date_ordered] = {"order_count" : 1, "price": y.orderprice, "total_products":y.total_products}
                    else:
                        order_success[y.date_ordered]["order_count"] += 1
                        order_success[y.date_ordered]["price"] += y.orderprice
                        order_success[y.date_ordered]["total_products"] += y.total_products
                else:
                    if not y.date_ordered in order_cancelled.keys():
                        order_cancelled[y.date_ordered] = {"order_count" : 1, "price": y.orderprice, "total_products":y.total_products}
                    else:
                        order_cancelled[y.date_ordered]["order_count"] += 1
                        order_cancelled[y.date_ordered]["price"] += y.orderprice
                        order_cancelled[y.date_ordered]["total_products"] += y.total_products

            context = {'order_success': order_success, 'order_cancelled': order_cancelled, 'success':success, 'fail':fail}
            return render(request, 'adminreport.html', context)
        else:
            today = date.today()
            status = Order.objects.filter(date_ordered=today, order_verify=True)
            failed = Order.objects.filter(date_ordered=today, order_verify=False)
            dictionary = {'success':status, 'fail':failed}
            return render(request, 'adminreport.html', dictionary)
    else:
        return redirect(admin_login)


# user side --------------------------------------------------------------------------------------------user side


# fuction used for loading userlogin
def user_login(request):
    if request.user.is_authenticated:
        return redirect(registered_user_home_page)
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=user_name).first()

        if user is not None and check_password(password,user.password):
            if user.is_active == False:
                messages.info(request, 'user is blocked')
                return redirect(user_login)
            else:
                auth.login(request, user)
                value = products.objects.all()
                return redirect(registered_user_home_page)
        else:   
            value={"username":user_name}
            messages.info(request, 'invalid credentials')
            return redirect(user_login)
    else:
        return render(request, 'userloginpage.html')
        
    


def check_phone(request):
    if request.user.is_authenticated:
        return redirect(registered_user_home_page)
    otp = 1
    if request.method == 'POST':
        phone_number = request.POST['phone']
        request.session['phone_number'] = phone_number
        
        if User.objects.filter(last_name=phone_number).exists():
            otp = 0
            # adding otp creation 
            phone_number = str(91) + phone_number
            url = "https://d7networks.com/api/verifier/send"

            payload = {'mobile': phone_number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
            files = [

            ]
            headers = {
            'Authorization': 'Token 13ff28cd8a3bc23d426420f75b84879c7f958c4c'
            # 'Authorization': 'Token 7b965deb9feaf5d0601c369eda9ff2e04c56d9ce'   
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            print(response.text.encode('utf8'))

            data=response.text.encode('utf8')
            datadict=json.loads(data)

            id=datadict['otp_id']
            request.session['id'] = id

             # //otp creation 
            return render(request, 'userloginotp.html', {'otp':otp})
        else:
            return render(request, 'userloginotp.html',{'otp':otp})
    else:
        return render(request, 'userloginotp.html', {'otp':otp})


def confirm_otp(request):
    if request.user.is_authenticated:
        return redirect(registered_user_home_page)
    else:
        if request.method == 'POST':
            otp_number = request.POST['otp']
            
            id_otp = request.session['id']
            url = "https://d7networks.com/api/verifier/verify"

            payload = {'otp_id': id_otp,
            'otp_code': otp_number}
            files = [
            ]
            headers = {
            'Authorization': 'Token 13ff28cd8a3bc23d426420f75b84879c7f958c4c'
            }
            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data)
            status=datadict['status']

            if status == 'success':
                phone_number = request.session['phone_number']  
                user = User.objects.filter(last_name=phone_number).first()
                if user is not None:
                    if user.is_active == False:
                        messages.info(request, 'user is blocked')
                        return redirect(user_login)
                    else:
                        auth.login(request, user)
                        # value = products.objects.all()
                        return redirect(registered_user_home_page)
                else:
                    return redirect(user_login)
                
            else:
                messages.error(request,'User not Exist')
                return redirect(user_login)

        else:
            return HttpResponse("oops")




# function for user logout
def user_logout(request):
    if request.user.is_authenticated:
       auth.logout(request)
       return redirect('/')
   

# function used to userregistrtaion
def user_registration(request):
    if request.user.is_authenticated:
        return redirect(registered_user_home_page)
    if request.method == 'POST':
        name = request.POST['name']
        user_name = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password1']    
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
                if User.objects.filter(username=user_name).exists():
                    messages.info(request, 'user name already exists')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already exists')
                return render(request, 'userregistration.html')
            else:
                user = User.objects.create_user(first_name=name, username=user_name, email=email, password=password, last_name=mobile)
                user.save()
                return redirect(user_login)
        else:
            messages.info(request, 'Password does not matching')
            return render(request, 'userregistration.html')
        

    else:      
        return render(request, 'userregistration.html')





# function to test user hom page
def user_home_page(request):
    if request.user.is_authenticated:
        return redirect(registered_user_home_page)
    else:
        value= products.objects.all()
        return render(request, 'userhomepagenew/index.html',{'value':value})
        


#function to get registered user home page
def registered_user_home_page(request):
    if request.user.is_authenticated:
        value= products.objects.all()
        user = request.user
        hai = 0
    
        return render(request, 'userhomepagenew/registereduser.html',{'value':value, 'user':user, 'hai':hai})
    else:
        return redirect(user_home_page)

def contact(request):
    if request.user.is_authenticated:
        value = 0
        return render(request, 'userhomepagenew/contact.html', {'value':value})
    else:
        value = 1 
        return render(request, 'userhomepagenew/contact.html', {'value':value})

def quickview(request, id):
    if request.user.is_authenticated:
        value = 0
        product = products.objects.filter(id=id).first()
        return render(request, 'userhomepagenew/single.html', {'product': product, 'value':value})
    else:
        value = 1
        product = products.objects.filter(id=id).first()
        return render(request, 'userhomepagenew/single.html', {'product': product, 'value':value})


def cart(request):
    
    if request.user.is_authenticated:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        total_price = 0
        for x in cart:
            total_price = total_price + x.get_total

        return render(request, 'userhomepagenew/cart.html', {'cart_data': cart, 'total_price':total_price})
    else:
        return redirect(user_home_page)





def add_cart(request, id):
    # print("----------------------------------entered add_cart function--------------------------")
    if request.user.is_authenticated:
        user = request.user
        product = products.objects.get(id=id)
        if OrderItem.objects.filter(product=product, user=user).exists():
            order = OrderItem.objects.get(product=product, user=user)
            if order.quantity <= order.product.quantity:
                order.quantity = order.quantity+1
                order.save()
                return redirect(cart)
            else:
                return redirect(registered_user_home_page)
        else:
            quantity = 1

            items = OrderItem.objects.create(user=user, product=product, quantity=quantity, total_price=product.price*quantity)
            return redirect(cart)
    else:
        return redirect(user_home_page)


def user_remove_Order_Item(request, id):
    if request.user.is_authenticated:
        b = OrderItem.objects.get(id=id)
        b.delete()
        # print("Deleted Order")
        return redirect(cart)
    else:
         return redirect(user_home_page)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        
        items = OrderItem.objects.filter(user=user)
        order = Order.objects.filter(user=user)
        address = ShippingAddress.objects.filter(user=user)
        
        
        total_price = 0
        for x in items  :
            total_price = total_price + x.get_total
        # razorpay integrate
        if request.method == "POST":

            order_amount = total_price*100
            order_currency = 'INR'
            client = razorpay.Client(auth = ('rzp_test_666QJpopWh4z27', 'Uci1HLeyYAs4mMBvKzysJL2X'))
            payment = client.order.create({'amount':order_amount, 'currency':order_currency, 'payment_capture': '1'})
        return render(request, 'userhomepagenew/checkout.html', {'items': items, 'order': order, 'total_price':total_price, 'user':user, 'address':address})
    else:
         return redirect(user_home_page)



def user_payment(request):
    # print("Entered user paymnet function ----------------------------")
    if request.user.is_authenticated:
        # print("Authenticated User")
        if request.method == 'POST':
            user = request.user
            address = request.POST['address1']
            state = request.POST['state']
            city = request.POST['city']
            zipcode = request.POST['zipcode']
            payment = request.POST['paymentMethod']
            # print(payment)
            mode = payment
            

            if ShippingAddress.objects.filter(address=address, state=state, city=city, zipcode=zipcode).exists():
                cart = OrderItem.objects.filter(user=user)
                date = datetime.datetime.now()
                transaction_id = uuid.uuid4()
                
            else:
                ShippingAddress.objects.create(user=user, address=address, state=state, city=city, zipcode=zipcode)
                cart = OrderItem.objects.filter(user=user)
                date = datetime.datetime.now()
                transaction_id = uuid.uuid4()

            address_instance = ShippingAddress.objects.get(address=address)
            for item in cart:
                Order.objects.create(user=user, address=address_instance, product=item.product,
                                     total_price=item.product.price*item.quantity,
                                     transaction_id=transaction_id, date_ordered=date,complete=True, payment_mode=mode, quantity=item.quantity)
                item.product.save()
            cart.delete()
            messages.info(request, "Placed Order")
            return JsonResponse('success',safe=False)
            # return redirect(registereduserhomepage)
            # return render(request, 'home/payment.html')
        else:

            # print("entered payment else conditioin")
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
    else:
         return redirect(user_home_page)


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        address = ShippingAddress.objects.filter(user=user)
        if ProfilePicture.objects.filter(user=user).exists():
            img=ProfilePicture.objects.get(user=user)
            return render(request, 'userhomepagenew/userprofile.html', {'value':user, 'img':img, 'address':address})
        return render(request, 'userhomepagenew/userprofile.html', {'value':user, 'address':address})
    else:
        return redirect(user_home_page)


def edit_profile_address(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            save_id = request.POST['id']
            save_address = request.POST['address']
            save_state = request.POST['state']
            save_city = request.POST['city']
            save_zipcode = request.POST['zipcode']
            if ShippingAddress.objects.filter(address=save_address, state=save_state, city=save_city, zipcode=save_zipcode):
                return redirect(profile)
            else:
                value = ShippingAddress.objects.get(id=save_id)
                value.address = save_address
                value.state = save_state
                value.city = save_city
                value.zipcode = save_zipcode
                value.save()
                return redirect(profile)
        else:
            return redirect(profile)  
    else:
        return redirect(user_home_page) 


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            user_name = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
        
            value = request.user
            value.first_name = name
            value.username = user_name
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
                
        
            return redirect(profile)
        else:
            return redirect(registered_user_home_page)
    else:
        return redirect(user_home_page)