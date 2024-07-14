# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Models Here 👇
class User(AbstractUser):
    TEAM_LEADER = 'team_leader'
    ADMINISTRATOR = 'administrator'
    AMBASSADOR = 'ambassador'
    MEMBER = "members"

    ROLE_CHOICES = [
        (TEAM_LEADER, 'Team Leader'),
        (ADMINISTRATOR, 'Administrator'),
        (AMBASSADOR, 'Ambassador'),
        (MEMBER, "Member"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
