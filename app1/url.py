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
    path('userlogin/', views.userlogin, name="userlogin"),
    path('userlogout/', views.userlogout, name="userlogout"),
    # path('userhome/', views.userhome, name="userhome"),
    path('categorymanagement', views.categorymanagement, name="categorymanagement"),
    path('addcategory/', views.addcategory, name="addcategory"),
    path('deletecategory/<int:id>', views.deletecategory, name='deletecategory'),
    #for testing
    # path('test/', views.test, name="test"),

    #user home pages
    path('nw_userhome', views.nw_userhome, name="nw_userhome"),
    path('', views.actual_userhome, name="actual_userhome"),
    # path('registereduser/', views.registereduser, name="registereduser"),
    # path('', views.userhomepage, name="userhomepage"),
    # path('quickview/', views.quickview, name="quickview"),
    # path('contact/', views.contact, name="contact"),
    # path('productof/', views.product, name="productof"),
    # path('checkout/', views.checkout, name="checkout"),
    # path('cart/', views.cart, name="cart"),

    #cart 
    path('updateitem/' ,views.updateitem, name="updateitem"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
   
    
]
