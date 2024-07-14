# teams/serializers.py
from rest_framework import serializers
from accounts.models import User
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    team_leader = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    ambassadors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'team_leader', 'ambassadors', 'members']
