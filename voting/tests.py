from django.test import TestCase
from django.contrib.auth.models import User
from voting.models import Vote
from match.models import Match
from players.models import Player  
from django.urls import reverse


# Create your tests here.
class SelfVoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="mark")
        self.match = Match.objects.create(user=self.user)

        self.p1 = Player.objects.create(
            name="A", age=25, position="Midfielder",
            user=self.user, shooting=5
        )

        self.match.players_in_match.set([self.p1])

    def test_self_vote_is_ignored(self):
        url = reverse('submit_votes', args=[self.match.share_token])

        self.client.post(url, {
            'voter_id': self.p1.id,
            'vote_motm': self.p1.id,  # attempt self-vote
        })

        self.assertEqual(Vote.objects.count(), 0)
        
class DoubleVoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="mark")
        self.match = Match.objects.create(user=self.user)

        self.p1 = Player.objects.create(
            name="A", age=25, position="Midfielder",
            user=self.user, shooting=5
        )
        self.p2 = Player.objects.create(
            name="B", age=30, position="Defender",
            user=self.user, shooting=5
        )

        self.match.players_in_match.set([self.p1, self.p2])

    def test_cannot_vote_twice(self):
        url = reverse('submit_votes', args=[self.match.share_token])

        # First vote
        self.client.post(url, {
            'voter_id': self.p1.id,
            'vote_motm': self.p2.id,
        })

        # Second attempt
        response = self.client.post(url, {
            'voter_id': self.p1.id,
            'vote_motm': self.p2.id,
        })

        self.assertTemplateUsed(response, 'alreadyvoted.html')

