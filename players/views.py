from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Player
from .forms import PlayerForm
import random

# Create your views here.
@login_required
def add_player(request):
    if request.method == 'POST':
        # Here you would handle form submission, validate data, and save the new player
        form = PlayerForm(request.POST)
        if form.is_valid():
            new_player = form.save(commit=False)
            new_player.user = request.user  # Associate player with the logged-in user
            new_player.save()
            messages.success(request, 'Player added successfully!')
            return redirect('viewplayers')  # Redirect to the list of players after adding
        else:
            messages.error(request, 'Please correct the errors below.')
            
        return redirect('viewplayers')  # Redirect to the list of players after adding
    else:
        form = PlayerForm()
    return render(request, 'newplayer.html', {'form': form})
    

@login_required
def view_players(request):
    players = Player.objects.filter(user=request.user)
    players = sorted(players, key=lambda p: p.overall(), reverse=True)
    return render(request, 'viewplayers.html', {'players': players})
 
 
@login_required
def delete_player(request):
    if request.method == 'POST':
        # Get the list of ticked player IDs from the form
        selected_ids = request.POST.getlist('selected_players')
 
        if not selected_ids:
            messages.error(request, 'No players selected. Tick a player first.')
            return redirect('viewplayers')
 
        # Only delete players that belong to the logged in user
        # The filter(user=request.user) is vital — stops anyone deleting someone else's players
        deleted = Player.objects.filter(id__in=selected_ids, user=request.user)
        count = deleted.count()
        deleted.delete()
 
        messages.success(request, f'{count} player(s) removed from your squad.')
 
    return redirect('viewplayers')

@login_required
def team_select(request):
    # List all player associated with the logged in user, sorted by overall rating
    players = Player.objects.filter(user=request.user)
    players = sorted(players, key=lambda p: p.overall(), reverse=True)
    return render(request, 'teamselect.html', {'players': players})



@login_required
def generated_teams(request):

    if request.method != 'POST':
        return redirect('generatedteams')
 
    selected_ids = request.POST.getlist('selected_players')
    
    # Validation: Ensure at least 2 players are selected
    if len(selected_ids) < 2:
        messages.error(request, 'Please select at least 2 players.')
        return redirect('teamselect')
 
    # Fetch the selected players, only from this user
    players = list(
        Player.objects.filter(id__in=selected_ids, user=request.user)
    )
 
   #TEAM BALACER ALGORITHM
   
   # Step 1 — sort players by position and overall rating
    
    defenders = sorted([p for p in players if p.position == 'Defender'], key=lambda p: p.overall(), reverse=True)
    midfielders = sorted([p for p in players if p.position == 'Midfielder'], key=lambda p: p.overall(), reverse=True)
    attackers = sorted([p for p in players if p.position == 'Attacker'], key=lambda p: p.overall(), reverse=True)
     
    ordered_groups = [attackers, midfielders, defenders]  # Attackers first, then midfielders, then defenders
    
    random.shuffle(ordered_groups)  # Shuffle Positions to stop attackers always being picked first
    
    group_order = [player for group in ordered_groups for player in group]  # add the players back into one list, but now in a randomised position order
    
    team_a = []
    team_b = []
 
   #Randomise which team gets the first pick, then alternate picks down the list of players until all players are assigned to a team
    
    first_pick = random.choice(['A', 'B'])
    
    for i, player in enumerate(group_order):
        if first_pick == "A": 
            if i % 2 == 0:
                team_a.append(player)
            else:
                team_b.append(player)
        else:  
            if i % 2 == 0:
                team_b.append(player)
            else:
                team_a.append(player)
         
        

    #Calculate total overall for each team by summing the overall of each player to see balance of teams.
    team_a_total = round(sum(p.overall() for p in team_a), 1)
    team_b_total = round(sum(p.overall() for p in team_b), 1)
 
 
    context = {
        'team_a':       team_a,
        'team_b':       team_b,
        'team_a_total': team_a_total,
        'team_b_total': team_b_total,
        
    }
    return render(request, 'generatedteams.html', context)
 