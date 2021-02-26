from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    study_year = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} Profile'