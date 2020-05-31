# from django.shortcuts import render
from rest_framework import viewsets

from .serializers import AutomationTargetSerializer
from .models import AutomationTarget


class AutomateTargetViewSet(viewsets.ModelViewSet):
    queryset = AutomationTarget.objects.all().order_by('name')
    serializer_class = AutomationTargetSerializer
