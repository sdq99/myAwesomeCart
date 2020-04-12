from rest_framework import viewsets
from . import models, serializers

class UsersDetailViewset(viewsets.ModelViewSet):
    queryset = models.UsersDetail.objects.all()
    serializer_class = serializers.UsersDetailSerializer
