from django.db import models
from accounts.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    team_leader = models.ForeignKey(User, related_name='led_teams', on_delete=models.CASCADE)
    ambassadors = models.ManyToManyField(User, related_name='teams_as_ambassador')
    members = models.ManyToManyField(User, related_name='teams_as_member')

    def __str__(self):
        return self.name
