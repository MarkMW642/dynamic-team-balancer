from django.db import models
from django.contrib.auth.models import User
import uuid
from collections import Counter


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches')
    created_at = models.DateTimeField(auto_now_add=True)
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    players_in_match = models.ManyToManyField('players.Player', related_name='matches', blank=True)
    voting_open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Match {self.id} created by {self.user.username} on {self.created_at.strftime('%d/%m/%Y')}"
    
    def close_voting(self):
        from voting.models import Vote
        
    # This tallys all votes together and applies dynamic rating upgrades to players with most votes
    # Voting closes after admin manually closes
        self.voting_open = False
        self.save()
        
        VOTE_UPGRADES = {
            'Man_of_the_Match': {'shooting': 0.2, 'passing': 0.2, 'defending': 0.2, 
                                 'stamina': 0.2, 'work_rate': 0.2,  
                                 'strength': 0.1, 'skills': 0.1, 'technical_ability': 0.1},
                                
            'Work_Horse': {'stamina': 0.2, 'work_rate': 0.2},
            'Playmaker': {'passing': 0.2, 'skills': 0.2},
            'Defensive_Wall': {'defending': 0.2, 'strength': 0.2},
            'Finisher': {'shooting': 0.2, 'technical_ability': 0.2},
        }
        
        ATTRIBUTE_FIELDS= ['shooting', 'passing', 'defending', 'stamina', 'work_rate', 
                            'pace', 'strength', 'skills', 'technical_ability']
        
        all_players = list(self.players_in_match.all())
        player_upgrade = set() #Tracks which players win which category
        
        for vote_type, stat_changes in VOTE_UPGRADES.items():
            votes = Vote.objects.filter(match=self, vote_type=vote_type)
            
            if not votes.exists():
                continue
            
            counts = Counter(votes.values_list('target__id', flat=True))
            max_votes = max(counts.values())
            
            winners = [pid for pid, count in counts.items() if count == max_votes]
            
            #This loop checks for players within match, and if player wins most votes, update attributes based on amount.
            for player in all_players:
                if player.id in winners:
                    player_upgrade.add((player.id))
                    for stat, amount in stat_changes.items():
                        current = getattr(player, stat)
                        
                        setattr(player, stat, min(10, round(current + amount, 1)))
                        
                    player.save()
                    
        #If player receives no votes, they get a small decrease to all attributes
        for player in all_players:
            if player.id not in player_upgrade:
                for stat in ATTRIBUTE_FIELDS:
                    current = getattr(player, stat)
                    setattr(player, stat, max(1, round(current - 0.05, 2)))
                player.save()
        
        self.voting_open = False
        self.save()
            
        
        
        
        
    
# Create your models here.
