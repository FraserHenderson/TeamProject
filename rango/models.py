from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

# Named UserEntity instead of User to prevent from clashing with code
# imported from django.contrib.auth.models
class UserEntity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    profile_picture = models.ImageField()
    login_status = models.BooleanField(default=False)
    followed_users = models.ManyToManyField("self", symmetrical=False)

    class Meta:
        verbose_name_plural = 'User Entities'
    
    def __str__(self):
        return self.name

class Medium(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    thumbnail = models.ImageField()
    publish_date = models.DateField()
    views = models.IntegerField()
    likes = models.IntegerField()
    medium_author = models.ForeignKey(UserEntity, on_delete=models.CASCADE)
    medium_category = models.ManyToManyField(MediaCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Media'
    
    def __str__(self):
        return self.name

class MediaCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Media Categories'
    
    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.CharField(max_length=200)
    upload_date = models.DateField()
    likes = models.IntegerField()
    reviewed_medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    review_author = models.ForeignKey(UserEntity, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text





#Old rango models for reference

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

    
class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

