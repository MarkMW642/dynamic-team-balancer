from django.test import TestCase
from django.contrib.auth.models import User
from voting.models import Vote
from match.models import Match
from players.models import Player   


# Create your tests here.
class DecayTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="mark")
        self.match = Match.objects.create(user=self.user)

        self.p1 = Player.objects.create(
            name="A",
            age = "32",
            position = "Midfielder",
            user=self.user,
            shooting=5)
        self.p2 = Player.objects.create(
            name="B",
            age="40",
            position = "Defender",
            user=self.user,
            shooting=5)

        self.match.players_in_match.set([self.p1, self.p2])

    def test_downgrade_applies(self):
        # p1 gets a vote, p2 gets none
        Vote.objects.create(match=self.match, voter=self.p1, target=self.p1, vote_type="Man_of_the_Match")

        self.match.close_voting()
        self.p2.refresh_from_db()

        self.assertLess(self.p2.shooting, 5)
        
    def test_upgrade_applies(self):
        old = self.p1.shooting

        Vote.objects.create(
        match=self.match,
        voter=self.p2,
        target=self.p1,
        vote_type="Man_of_the_Match"
    )

        self.match.close_voting()
        self.p1.refresh_from_db()

        self.assertGreater(self.p1.shooting, old)

