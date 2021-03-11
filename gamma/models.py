from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import datetime

# user profile model with all the required fields
class UserProfile(models.Model):
    YEAR_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    study_year = models.IntegerField(choices = YEAR_CHOICES) # the year of study the user is currently in 
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') # profile picture
    points = models.IntegerField(default=0) #total points of user
    tc = models.BooleanField()

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    def save(self):
        super().save()

        # resizing images that are uploaded as a profile picture for better performance of webapp
        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'pk': self.pk}) #


# model of posts with all required fields
class Post(models.Model):
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
    header_image = models.ImageField(default='whiteplaceholder.jpg', upload_to="images/")
    type = models.TextField(choices = ACTIVITIES)
    description = models.TextField() #User can provide a custom description of their activity
    distance = models.FloatField() #User can provide a custom distance of their activity
    time = models.DurationField() #Users can enter a period of time for how long their activity took
    measurement = models.TextField(choices = MKM) #user will be able to enter a distance and choose whether it is saved as miles or kilometers
    rating = models.IntegerField(default=0) #User can give their workout a "rating" of how well they feel it went
    date_posted = models.DateTimeField(default=timezone.now) #get the time/date created
    author = models.ForeignKey(User, on_delete=models.CASCADE) #This is important because it uses a foreign key to ensure that the post belongs to a user
                                                            #and if user is deleted then their post will also be deleted

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) #This will ensure that once a post is created the user will be redirected back to the post created

    def save(self):
        super().save()

        # resizing images that are uploaded as a profile picture for better performance of webapp
        img = Image.open(self.header_image.path)

        if img.height > 450 or img.width > 450:
            output_size = (450, 450)
            img.thumbnail(output_size)
            img.save(self.header_image.path)


# model for comments
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # comment will include its author
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # comment will show at the post that was commented on
    date_posted = models.DateTimeField(default=timezone.now) # comment will include date posted
    content = models.TextField(default="") # comment will include the content entered by the user
    is_rating = models.BooleanField(default=False) # adding a comment will not add points to the post's author

    def __str__(self):
        return f"{self.author}\'s Comment ({self.id}) on Post {self.post.id}"


# model for rating a post
class PostRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # rating will include its author
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # rating will show at the post that was rated
    rating = models.IntegerField(default=0,  # the choices that can be chosen for a rating
        choices =  (
            (0, 0),
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