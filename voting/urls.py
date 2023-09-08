from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.loginVoter, name='login-voter'),
    path('logout/', views.logoutVoter, name='logout-voter'),
    path('vote-main-office/', views.voteMainOffice, name='vote-main-office'),
    path('vote-choir-office/', views.voteChoirOffice, name='vote-choir-office'),
    path('vote-cma-cla-office/', views.voteCmaClaOffice, name='vote-cma-cla-office'),
    path('vote-scc-leaders/', views.voteSccLeaders, name='vote-scc-leaders'),
    path('add-main-office-vote/', views.addMainOfficeVote, name='add-main-office-vote'),
    path('add-choir-office-vote/', views.addChoirOfficeVote, name='add-choir-office-vote'),
    path('add-cma-leaders-vote/', views.addCmaLeadersVote, name='add-cma-leaders-vote'),
    path('add-cla-leaders-vote/', views.addClaLeadersVote, name='add-cla-leaders-vote'),
    path('add-scc-leaders-vote/', views.addSccLeadersVote, name='add-scc-leaders-vote'),
    path('results/', views.results, name='results'),
]