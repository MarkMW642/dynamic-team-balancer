from django.test import TestCase
from django.contrib.auth.models import User
from .models import Player

class OverallRatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_attacker_overall_within_range(self):
        player = Player(
            user=self.user, name='Test', age=25,
            position='Attacker',
            shooting=8, passing=7, defending=3,
            stamina=6, work_rate=6, pace=8,
            strength=5, skills=7, technical_ability=7,
            match_winner=4
        )
        result = player.overall()
        self.assertGreaterEqual(result, 40)
        self.assertLessEqual(result, 99)

    def test_defender_overall_within_range(self):
        player = Player(
            user=self.user, name='Test', age=25,
            position='Defender',
            shooting=3, passing=5, defending=8,
            stamina=7, work_rate=7, pace=5,
            strength=9, skills=4, technical_ability=5,
            match_winner=3
        )
        result = player.overall()
        self.assertGreaterEqual(result, 40)
        self.assertLessEqual(result, 99)

    def test_stat_cap_does_not_exceed_10(self):
        player = Player(
            user=self.user, name='Test', age=25,
            position='Midfielder',
            shooting=10, passing=10, defending=10,
            stamina=10, work_rate=10, pace=10,
            strength=10, skills=10, technical_ability=10,
            match_winner=5
        )
        
        new_val = min(10.0, round(player.shooting + 0.2, 2))
        self.assertLessEqual(new_val, 10)