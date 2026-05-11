from django.urls import path
from . import views

urlpatterns = [
    path('newplayer/', views.add_player, name='newplayer'),
    path('players/',   views.view_players,  name='viewplayers'),
    path('delete/',     views.delete_player, name='deleteplayer'),
    path('teamselect/',   views.team_select, name='teamselect'),
    path('teamselect/generatedteams/', views.generated_teams, name='generatedteams'),
]