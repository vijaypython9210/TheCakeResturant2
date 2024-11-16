from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('frontPage',views.frontPage,name='frontPage'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('collections',views.collections,name='collections'),
    path('products',views.products,name='products'),
    path('category/<int:id>',views.category,name='category'),
    path('product/<int:id>',views.product_details,name='product_details'),
    # path('getAllProducts',views.getAllProducts,name='getAllProducts'),
    path('cart/<int:id>',views.cart,name='cart'),
    path('favourite/<int:id>',views.favourite,name='favourite'),
    path('cartDetails/',views.cartDetails,name='cartDetails'),
    path('favouriteDetails/',views.favouriteDetails,name='favouriteDetails'),
    path('deleteProductFromCart/<int:id>',views.deleteProductFromCart,name='deleteProductFromCart'),
    path('deleteAllFavourite/',views.deleteAllFavourite,name='deleteAllFavourite'),
    path('deleteAllCart/',views.deleteAllCart,name='deleteAllCart')

]