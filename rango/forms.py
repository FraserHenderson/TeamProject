from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile, Medium


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class MediumForm(forms.ModelForm):
    name = forms.CharField(max_length=50,)
    description = forms.CharField(max_length=200,)
    thumbnail = forms.ImageField()
    #publish_date = forms.DateTimeField(default=datetime.strptime((str(datetime.now()))[:19], '%Y-%m-%d %H:%M:%S'))
    #views = forms.IntegerField(default=0)
    #likes = forms.IntegerField(default=0)
    #medium_author = forms.ForeignKey(UserEntity, on_delete=models.CASCADE)
    #medium_category = forms.ForeignKey(MediaCategory, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        model = Medium
        fields = ('name', 'description', 'thumbnail',)
    
                             
        
