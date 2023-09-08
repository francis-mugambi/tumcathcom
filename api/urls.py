from django.urls import path
from .import views

urlpatterns = [
    path('', views.getRoute, name="route"),
    path('customers/<str:str>/', views.customer, name="customer"), 
    path('customers/', views.customers, name="customers"),       
]