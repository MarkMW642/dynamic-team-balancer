from django.urls import path
from . import views

urlpatterns=[
    path('savematch/', views.save_match, name='savematch'),
    path('closevoting/<uuid:token>/', views.close_voting, name='closevoting'),
    
]
