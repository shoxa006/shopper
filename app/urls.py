from django.urls import path
from app.views.activate_mail import ActivateEmailView
from app.views.index import shop_view, shopping_cart, checkout, contact, \
    update_product, delete_product, IndexPage, ProductDetailsPage, CreateProductPage
from app.views.auth import LoginPage, logout_view, RegisterPage, ForgotPasswordView


urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('product-details/<int:product_id>', ProductDetailsPage.as_view(), name='shop-details'),
    path('shop/', shop_view, name='shop'),
    path('shopping-cart/', shopping_cart, name='shopping-cart'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),

    path('create-product/', CreateProductPage.as_view(), name='create-product'),
    path('update-product/<int:product_id>', update_product, name='update-product'),
    path('delete-product/<int:product_id>', delete_product, name='delete-product'),

    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('activate/<str:uid>/<str:token>', ActivateEmailView.as_view(), name='confirm-mail'),
]
