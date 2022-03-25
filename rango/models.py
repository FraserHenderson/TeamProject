from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

import datetime
from datetime import datetime

# Create your models here.

# Named UserEntity instead of User to prevent from clashing with code imported from django.contrib.auth.models
class UserEntity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    profile_picture = models.ImageField(blank=True)
    followed_users = models.ManyToManyField("self", symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = 'User Entities'
    
    def __str__(self):
        return self.name

class MediaCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Media Categories'
    
    def __str__(self):
        return self.name

class Medium(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, default='')
    thumbnail = models.ImageField()
    publish_date = models.DateTimeField(default=datetime.strptime((str(datetime.now()))[:19], '%Y-%m-%d %H:%M:%S'))
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    medium_author = models.ForeignKey(UserEntity, on_delete=models.CASCADE)
    medium_category = models.ForeignKey(MediaCategory, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Media'
    
    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.CharField(max_length=200)
    upload_date = models.DateTimeField(default=datetime.strptime((str(datetime.now()))[:19], '%Y-%m-%d %H:%M:%S'))
    likes = models.IntegerField(default=0)
    reviewed_medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    review_author = models.ForeignKey(UserEntity, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

