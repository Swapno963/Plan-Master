from rest_framework import serializers
from . import models

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tasks
        fields = '__all__'