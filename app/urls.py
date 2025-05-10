# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # basic homepage view
    path('technology/', views.technology, name='technology'),
    path('product/', views.product_view, name='product'),
    path('about/', views.about, name='about'),
    path('contact-success/', views.contact_success, name='contact_success'),
    # Add more paths as needed
]
