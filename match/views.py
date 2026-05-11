from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Match
from players.models import Player


# Create your views here.
@login_required
def save_match(request):
    if request.method != 'POST':
        return redirect('dashboard')
    
    selected_ids = request.POST.getlist('player_ids')
    
    if not selected_ids:
        messages.error(request, 'No players selected. Tick a player first.')
        return redirect('dashboard')
        
    match = Match.objects.create(user=request.user)
        
    players = Player.objects.filter(id__in=selected_ids, user=request.user)
    match.players_in_match.set(players)
    match.save()
    messages.success(request, 'Match Saved Successfully!')
    
    share_url = request.build_absolute_uri(f'/voting/{match.share_token}/')
    
    return render(request, 'savematch.html', {
        'share_url': share_url,
        'match': match,
        'players': players,
        })
    
    
    
@login_required
def close_voting(request, token):
    match = get_object_or_404(Match, share_token=token, user=request.user)
    
    if not match.voting_open:
        messages.error(request, 'Voting is Already Closed For This Match.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        match.close_voting()
        messages.success(request, 'Voting Closed & Players Updated Successfully!')
        return redirect('dashboard')
    
    return render(request, 'closevoting.html', {'match': match})