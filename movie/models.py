from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=50)
    moviePlatform=models.ForeignKey('StreamPlatform',related_name='stream',on_delete=models.CASCADE)
    avg_rating=models.FloatField(default=0)
    people_rating=models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=False)
    def __str__(self):
        return self.name
class StreamPlatform(models.Model):
    name=models.CharField(max_length=20)
    about = models.CharField(max_length=20)
    url=models.URLField(max_length=200)
    def __str__(self):
        return self.name
class review(models.Model):
    rate=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    review_comment=models.TextField(max_length=50)
    review_author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    review_movie=models.ForeignKey(Movie,related_name="review",on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)