from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class UserProfile(models.Model):
    YEAR_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    study_year = models.IntegerField(choices = YEAR_CHOICES)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'pk': self.pk}) #

class Post(models.Model):
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )
    ACTIVITIES = ( #The various activities that a user can choose from when making a post
        ("Run", "Run"),
        ("Cycle", "Cycle"),
        ("Swim", "Swim"),
        ("HIIT", "HIIT"),
        ("Weight Training", "Weight Training")
    )
    MKM = (
        ("N/A", "N/A"), #won't always be neccessary to have a distance
        ("km", "km"),
        ("m", "m")
    )
    title = models.CharField(max_length=100)
    type = models.TextField(choices = ACTIVITIES)
    description = models.TextField() #User can provide a custom description of their activity
    distance = models.FloatField()
    measurement = models.TextField(choices = MKM) #user will be able to enter a distance and choose whether it is saved as miles or kilometers
    rating = models.IntegerField(choices = RATING) #User can give their workout a "rating" of how well they feel it went
    date_posted = models.DateTimeField(default=timezone.now) #get the time/date created
    author = models.ForeignKey(User, on_delete=models.CASCADE) #This is important because it uses a foreign key to ensure that the post belongs to a user
                                                #and if user is deleted then their post will also be deleted
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) #This will ensure that once a post is created the user will be redirected back to the post created