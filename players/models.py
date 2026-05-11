from django.db import models
from django.contrib.auth.models import User
 
 
class Player(models.Model):
    POSITION_CHOICES = [
        ('Defender',   'Defender'),
        ('Midfielder', 'Midfielder'),
        ('Attacker',   'Attacker'),
    ]
 
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='players')
    name         = models.CharField(max_length=100)
    age          = models.PositiveIntegerField()
    position     = models.CharField(max_length=20, choices=POSITION_CHOICES)
 
    # Attributes 1-10
    shooting          = models.FloatField(default=5)
    passing           = models.FloatField(default=5)
    defending         = models.FloatField(default=5)
    stamina           = models.FloatField(default=5)
    work_rate         = models.FloatField(default=5)
    pace              = models.FloatField(default=5)
    strength          = models.FloatField(default=5)
    skills            = models.FloatField(default=5)
    technical_ability = models.FloatField(default=5)
 
    # Match winner 1-5
    match_winner = models.PositiveIntegerField(default=3)
 
    # Dynamic rating - starts at 65, adjusted by votes later
    rating = models.FloatField(default=65.0)
 
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"{self.name} ({self.position}) — {self.user.username}"
 
    def overall(self):
    
 
        if self.position == 'Attacker':
            score = (
                self.shooting          * 0.25 +
                self.passing           * 0.10 +
                self.defending         * 0.05 +
                self.stamina           * 0.10 +
                self.work_rate         * 0.05 +
                self.pace              * 0.15 +
                self.strength          * 0.05 +
                self.skills            * 0.10 +
                self.technical_ability * 0.10 
            )
            
        elif self.position == 'Defender':
            score = (
                self.shooting          * 0.05 +
                self.passing           * 0.10 +
                self.defending         * 0.25 +
                self.stamina           * 0.15 +
                self.work_rate         * 0.10 +
                self.pace              * 0.10 +
                self.strength          * 0.25 +
                self.skills            * 0.05 +
                self.technical_ability * 0.10 

            )
        else:  # Midfielder
            score = (
                self.shooting          * 0.10 +
                self.passing           * 0.20 +
                self.defending         * 0.10 +
                self.stamina           * 0.15 +
                self.work_rate         * 0.15 +
                self.pace              * 0.10 +
                self.strength          * 0.05 +
                self.skills            * 0.10 +
                self.technical_ability * 0.10 
            )
        
        
        base = 30 + (score * 5.9)
        
        mw_bonus = self.match_winner * 1.5
        
        return round(min(base + mw_bonus, 99), 1)
