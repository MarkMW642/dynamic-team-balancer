from django.db import models


# Create your models here.
class Vote(models.Model):
    VOTE_TYPE_CHOICES = [
        ('Man_of_the_Match', 'Man of the Match'),
        ('Work_Horse', 'Work Horse'),
        ('Playmaker', 'Playmaker'),
        ('Defensive_Wall', 'Defensive Wall'),
        ('Finisher', 'Finisher'),
    ]
    
    match = models.ForeignKey('match.Match', on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='votes')
    target = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='received_votes')
    vote_type = models.CharField(max_length=20, choices=VOTE_TYPE_CHOICES)
    
    class Meta:
        unique_together = ('match', 'voter', 'vote_type')  # Prevent multiple votes of same type by same voter in a match
        
        def __str__(self):
            return f'{self.voter.name} voted {self.vote_type} for {self.target.name} in Match {self.match.id}'