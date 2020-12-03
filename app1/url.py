from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('adminlogin/', views.adminlogin, name="adminlogin"),   
    path('admindashboard', views.admindashboard, name="admindashboard"),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('register/', views.userregistration, name="register"),
    path('productmanagement/', views.productmanagement, name="productmanagement"),  
    path('addproduct/', views.addproduct, name='addproduct'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name="update"),
    path('usermanagemnet', views.usermanagemnet, name="usermanagemnet"),
    path('deleteuser/<int:id>', views.deleteuser, name='deleteuser'),
    path('adduser/', views.adduser, name="adduser"),
    path('edituser/<int:id>', views.edituser, name='edituser'),
    path('updateuser/<int:id>', views.updateuser, name="updateuser"),
    path('adminlogout/', views.adminlogout, name="adminlogout"),
    
    
  
    path('categorymanagement', views.categorymanagement, name="categorymanagement"),
    path('addcategory/', views.addcategory, name="addcategory"),
    path('deletecategory/<int:id>', views.deletecategory, name='deletecategory'),
    path('manage-order/', views.manage_order, name="manage_order"),
    path('delete_order/<int:id>', views.delete_order, name="delete_order"),
    path('cancel_order/<int:id>', views.cancel_order, name="cancel_order"),
    path('report/', views.report, name="report"),
     path('block_user/<int:id>', views.block_user, name="block_user"),



  

    #user home pages ------------------------------------------------------------------------------------------------------------------------------
    


    path('', views.userhomepage, name="userhomepage"),
    path('registereduserhomepage', views.registereduserhomepage, name="registereduserhomepage"),
    path('contact/', views.contact, name="contact"),
    path('quickview/<int:id>', views.quickview, name="quickview"),
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('userlogout/', views.userlogout, name="userlogout"),
    path('add-cart/<int:id>', views.add_cart, name="add_cart"),
    path('user-removeOrderItem/<int:id>', views.user_removeOrderItem, name="user_removeOrderItem"),
    path('user_payment/', views.user_payment, name="user_payment"),
    path('user-order/', views.user_order, name="user_order"),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('edit_profile_address/', views.edit_profile_address, name="edit_profile_address"),
    path('check_phone/', views.check_phone, name="check_phone"),
    path('confirm_otp', views.confirm_otp, name="confirm_otp"),


    
]
