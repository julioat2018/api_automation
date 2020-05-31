from rest_framework import serializers

from .models import AutomationTarget


class AutomationTargetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AutomationTarget
        fields = ['name']
