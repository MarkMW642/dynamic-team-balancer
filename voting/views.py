from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from match.models import Match
from .models import Vote
from players.models import Player


# Create your views here.
def vote_page(request, token):
    match = get_object_or_404(Match, share_token=token)
    
    if not match.voting_open:
        return render(request, 'votingclosed.html', {'match': match})
    
    players = match.players_in_match.all() 
  
    return render(request, 'placevotes.html', {
        'match': match, 
        'players': players,
        'token': token,
        })
    
        
  
    
def submit_vote(request, token):
    if request.method != 'POST':
        return redirect('placevotes', token=token)

    match = get_object_or_404(Match, share_token=token)

    if not match.voting_open:
        return render(request, 'votingclosed.html', {'match': match})
    
    
    voter_id = request.POST.get('voter_id')
    if not voter_id:
        messages.error(request, 'Please select yourself first.')
        return redirect('placevotes', token=token)

    voter = get_object_or_404(Player, id=voter_id)

    if voter not in match.players_in_match.all():
        messages.error(request, 'You are not listed in this match.')
        return redirect('placevotes', token=token)
    
    if Vote.objects.filter(match=match, voter=voter).exists():
        return render(request, 'alreadyvoted.html')


    # Each vote type maps to a form field name
    VOTE_FIELDS = {
        'Man_of_the_Match':'vote_motm',
        'Work_Horse':  'vote_workhorse',
        'Defensive_Wall': 'vote_defensive_wall',
        'Playmaker':  'vote_playmaker',
        'Finisher':   'vote_finisher',
    }

    votes_to_create = []

    for vote_type, field_name in VOTE_FIELDS.items():
        target_id = request.POST.get(field_name)

        # Skip if no player was selected for this category
        if not target_id:
            continue

        # Skip if they tried to vote for themselves
        if str(target_id) == str(voter.id):
            continue

        try:
            target = Player.objects.get(id=target_id, )
        except Player.DoesNotExist:
            continue

        votes_to_create.append(Vote(
            match=match,
            voter=voter,
            target=target,
            vote_type=vote_type,
        ))

    Vote.objects.bulk_create(votes_to_create, ignore_conflicts=True)
    
    return render(request, 'votethanks.html', {'match': match})


        
   
        
    