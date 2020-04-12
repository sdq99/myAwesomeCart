from django.db import models

# Create your models here.
class UsersDetail(models.Model):
    # userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50)