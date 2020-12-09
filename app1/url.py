from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('admin-login/', views.admin_login, name="admin-login"),   
    path('admin-dashboard', views.admin_dashboard, name="admin-dashboard"),
   
    
    path('product-management/', views.product_management, name="product-management"),  
    path('add-product/', views.add_product, name='addproduct'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name="update"),
    path('user-managemnet', views.user_managemnet, name="usermanagemnet"),
    path('delete-user/<int:id>', views.delete_user, name='deleteuser'),
    path('add-user/', views.add_user, name="adduser"),
    path('edit-user/<int:id>', views.edit_user, name='edituser'),
    path('block-user/<int:id>', views.block_user, name="block_user"),
    path('update-user/<int:id>', views.update_user, name="updateuser"),
    path('admin-logout/', views.admin_logout, name="admin-logout"),
    
    
  
    path('category-management', views.category_management, name="categorymanagement"),
    path('add-category/', views.add_category, name="addcategory"),
    path('delete-category/<int:id>', views.delete_category, name='deletecategory'),
    path('manage-order/', views.manage_order, name="manage_order"),
    path('delete-order/<int:id>', views.delete_order, name="delete_order"),
    path('cancel-order/<int:id>', views.cancel_order, name="cancel_order"),
    path('report/', views.report, name="report"),
  


  

    #user home pages ------------------------------------------------------------------------------------------------------------------------------
    

    # path('user-login/', views.user_login, name="userlogin"),
    path('', views.user_home_page, name="userhomepage"),
    path('registered-user-home-page', views.registered_user_home_page, name="registereduserhomepage"),
    path('contact/', views.contact, name="contact"),
    path('quickview/<int:id>', views.quickview, name="quickview"),
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('user-login/', views.user_login, name="userlogin"),
    path('register/', views.user_registration, name="register"),
    path('user-logout/', views.user_logout, name="userlogout"),
    path('add-cart/<int:id>', views.add_cart, name="add_cart"),
    path('user-removeOrderItem/<int:id>', views.user_remove_Order_Item, name="user_removeOrderItem"),
    path('user_payment/', views.user_payment, name="user_payment"),
    path('user-order/', views.user_order, name="user_order"),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('edit_profile_address/', views.edit_profile_address, name="edit_profile_address"),
    path('check-phone/', views.check_phone, name="check_phone"),
    path('confirm-otp', views.confirm_otp, name="confirm_otp"),
    # path('cart/update/<int:id>', views.cart_update, name="cart_update"),


    
]
