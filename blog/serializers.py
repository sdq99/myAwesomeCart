from rest_framework import serializers
from . import models

class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UsersDetail
        fields = ('id', 'userName')