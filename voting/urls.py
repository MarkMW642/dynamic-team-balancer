from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:token>/',        views.vote_page,     name='vote_page'),
    path('<uuid:token>/submit/', views.submit_vote,  name='submit_votes'),
]
