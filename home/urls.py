from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='index'),    
    path('leadership/', views.leadership, name='leadership'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<str:str>/', views.blogIteam, name='blog'),
    path('scc-leaders/', views.scc_leaders, name='scc-leaders'),
    path('photos/', views.photos, name='photos'),   
    path('videos/', views.videos, name='videos'),
    path('contacts/', views.contact, name='contact'),
    
]