from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import datetime

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
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

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
    POINTS = (
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (60, 60),
        (70, 70),
        (80, 80),
        (90, 90),
        (100, 100),
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
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    type = models.TextField(choices = ACTIVITIES)
    description = models.TextField() #User can provide a custom description of their activity
    distance = models.FloatField()
    time = models.DurationField() #Users can enter a period of time for how long their activity took
    measurement = models.TextField(choices = MKM) #user will be able to enter a distance and choose whether it is saved as miles or kilometers
    rating = models.IntegerField(choices = RATING) #User can give their workout a "rating" of how well they feel it went
    date_posted = models.DateTimeField(default=timezone.now) #get the time/date created
    author = models.ForeignKey(User, on_delete=models.CASCADE) #This is important because it uses a foreign key to ensure that the post belongs to a user
                                                            #and if user is deleted then their post will also be deleted
    points = models.IntegerField(choices=POINTS, default=0)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) #This will ensure that once a post is created the user will be redirected back to the post created

    def save(self):
        super().save()

        img = Image.open(self.header_image.path)

        if img.height > 450 or img.width > 450:
            output_size = (450, 450)
            img.thumbnail(output_size)
            img.save(self.header_image.path)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField(default="")
    rating = models.IntegerField(default=0,
        choices =  (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10)
        )
    )

    def __str__(self):
        return f"{self.author}\'s Comment ({self.id}) on Post {self.post.id}"