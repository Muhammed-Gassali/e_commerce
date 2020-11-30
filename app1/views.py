from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import products,category,Order,OrderItem,ShippingAddress,ProfilePicture   
from django.http import JsonResponse
import json
import datetime
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
        users = User.objects.all().count()
        order = Order.objects.all().count()
        product = products.objects.all().count()
        context ={'users':users,'order':order, 'products':product}
        return render(request, 'admindashboard.html',context)
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


def block_user(request, id):
    if request.session.has_key('adminusername'):
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
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

def cancel_order(request, id):
    if request.session.has_key('adminusername'):
        b = Order.objects.get(id=id)
        b.order_verify = False
        b.save()
        return redirect(manage_order)
    else:
        return redirect(adminlogin)

def report(request):
    if request.session.has_key('adminusername'):
        if request.method == "POST":
            print("entered ***************************************")
            start = request.POST['start_date']
            end = request.POST['end_date']
            order_dates = Order.objects.filter(date_ordered__range=[start,end]).count()
            context = {'order_dates':order_dates}
            print(start)
            return render(request, 'adminreport.html', context)
        else:
            return render(request, 'adminreport.html')
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

            
        user = User.objects.filter(username=username).first()

        if user is not None and check_password(password,user.password):
            if user.is_active == False:
                messages.info(request, 'user is blocked')
                return redirect('userlogin')
            else:
                auth.login(request, user)
                value = products.objects.all()
                return redirect('registereduserhomepage')
        else:   
            value={"username":username}
            messages.info(request, 'invalid credentials')
            return redirect('userlogin')
    else:
        return render(request, 'userloginpage.html')
    


def check_phone(request):
    if request.user.is_authenticated:
        return redirect('registereduserhomepage')
    otp = 1
    if request.method == 'POST':
        phone_number = request.POST['phone']
        request.session['phone_number'] = phone_number
        print(phone_number)
        if User.objects.filter(last_name=phone_number).exists():
            otp = 0
            print("success")
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
            print(payload)
            print(response.text.encode('utf8'))

            data=response.text.encode('utf8')
            datadict=json.loads(data)
            print('datadict:',datadict)

            id=datadict['otp_id']
            print('id:',id)
            request.session['id'] = id

             # //otp creation 
            return render(request, 'userloginotp.html', {'otp':otp})
        else:
            return render(request, 'userloginotp.html',{'otp':otp})
    else:
        return render(request, 'userloginotp.html', {'otp':otp})


def confirm_otp(request):
    if request.user.is_authenticated:
        return redirect('registereduserhomepage')
    else:
        if request.method == 'POST':
            otp_number = request.POST['otp']
            print(otp_number)
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
                        return redirect('userlogin')
                    else:
                        auth.login(request, user)
                        # value = products.objects.all()
                        return redirect('registereduserhomepage')
                else:
                    return redirect(userlogin)
                
            else:
                messages.error(request,'User not Exist')
                return redirect(userlogin)

        else:
            return HttpResponse("oops")









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
        address = ShippingAddress.objects.filter(user=user)
        
        
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
            order_amount = float(total_price)
            order_amount *= 100
            order_currency = 'USD'
            order_reciept = 'order_rcptid_11'
            notes = {'shipping address ':'noormahal''kerala'}
            response = client.order.create(dict(amount=order_amount, currency=order_currency, reciept=order_reciept, notes=notes, payment_capture='0'))
            # payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
            # order_id = response['id']
            # order_status = response['status']
            # if order_status=='created':
            #     context['product_id'] = product
            #     context['order_id'] = order_id
            #     return render(request, 'userhomepagenew/checkout.html', {'items': items, 'order': order, 'total_price':total_price, 'user':user, 'address':address}, context)


        return render(request, 'userhomepagenew/checkout.html', {'items': items, 'order': order, 'total_price':total_price, 'user':user, 'address':address})
    else:
        return render(request, 'userhomepagenew/index.html')


def user_payment(request):
    print("Entered user paymnet function ----------------------------")
    if request.user.is_authenticated:
        print("Authenticated User")
        if request.method == 'POST':
            user = request.user
        
            address = request.POST['address1']
            state = request.POST['state']
            city = request.POST['city']
            zipcode = request.POST['zipcode']
            print(address)

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
        print("hhhhhhhhhhhhhhhhhhhhhhhhhh############")
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
        address = ShippingAddress.objects.filter(user=user)

        # editing address 
        # if request.method=="POST":
        #     save_address = request.POST['address']
        #     save_state = request.POST['state']
        #     save_city = request.POST['city']
        #     save_zipcode = request.POST['zipcode']
        #     print(save_address)
        #     if ShippingAddress.objects.filter(address=save_address, state=save_state, city=save_city, zipcode=save_zipcode):
        #         return render(request, 'userhomepagenew/userprofile.html', {'value':user, 'img':img, 'address':address})
        #     else:
        #         value = ShippingAddress.objects.get(user=user)
        #         value.address = save_address
        #         value.state = save_state
        #         value.city = save_city
        #         value.zipcode = save_zipcode
        #         value.save()
        return render(request, 'userhomepagenew/userprofile.html', {'value':user, 'img':img, 'address':address})
    else:
        return redirect(userhomepage)


def edit_profile_address(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            save_id = request.POST['id']
            print("987697846937462913847387629837566")
            print(save_id)
            save_address = request.POST['address']
            save_state = request.POST['state']
            save_city = request.POST['city']
            save_zipcode = request.POST['zipcode']
            print(save_address)
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