from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('dasboard/', views.adminDashboard, name="admin-dashboard"), 
    path('members/', views.members, name="members"),    
    path('members/<str:str>/', views.deleteMember, name="delete-member"),   
    path('approve-id/', views.approveId, name="approve-id"),    
    path('approve/<str:str>/', views.approve, name="approve"), 
    path('unapprove/<str:str>/', views.unapprove, name="unapprove"), 
    path('messages/<str:str>/', views.deleteMessage, name="delete-message"),
    path('members/<str:str>/view', views.viewMember, name="view-member"), 
    path('generate-csv', views.generateCsv, name="generate-csv"), 
    path('generate-pdf', views.generatePdf, name="generate-pdf"), 
    path('voting-results', views.votingResults, name="voting-results"), 
    path('main-office-results', views.mainOfficeResults, name="main-office-results"), 
    path('choir-office-results', views.choirOfficeResults, name="choir-office-results"), 
    path('scc-leaders-results', views.sccLeadersResults, name="scc-leaders-results"), 
    path('cma-cla-leaders-results', views.cmaClaLeadersResults, name="cma-cla-leaders-results"), 
    path('authenticate-voting/', views.authenticateElection, name="authenticate-voting"),     
    path('authenticate-editing/', views.authenticateEditing, name="authenticate-editing"),    

    path('login/', views.login, name="login-admin"),       
    path('password-reset/', views.password_reset, name="password-reset-admin"), 
    path('password-reset-otcp/<str:str>/', views.password_reset_otcp, name="password-reset-otcp-admin"),  
    path('logout/', views.logout, name="logout-admin"),       
]