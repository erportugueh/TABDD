from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('homeUser/', views.homeUser,name='homeUser'), # Página inicial para user com account 
    path('register/', views.register, name='register'),  # Página de registro
    path('login/', views.login, name='login'),  # Página de login
    path('cart/', views.cart, name='cart'),  # Página do carrinho
   
]
