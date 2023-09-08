from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.login, name="login"),     
    path('signup/', views.signup, name="signup"),  
    path('password-reset/', views.password_reset, name="password-reset"), 
    path('password-reset-otcp/<str:str>/', views.password_reset_otcp, name="password-reset-otcp"),
    path('password-change/', views.password_change, name="password-change"),  
    path('profile/', views.profile, name="profile"),   
    path('print-id/', views.print_id, name="print-id"), 
    path('request-approval/<str:str>/', views.requestApproval, name="request-approval"),   
    path('download-card/<str:str>/', views.downloadCard, name="download-card"), 
    path('print-card/<str:str>/', views.printCard, name="print-card"),
    path('generate-cv/<str:str>/', views.generateCV, name="generate-cv"),
    path('news-events/', views.news_events, name="news-events"),  
    path('leaders/', views.leaders, name="leaders"),   
    path('logout/', views.logout, name="logout"),   
    path('update-profile-picture/', views.updateProfilePicture, name="update-profile-picture"),  
    
]