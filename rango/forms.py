from django import forms
from django.contrib.auth.models import User
from rango.models import UserProfile, UserEntity, MediaCategory, Medium


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )

class CategoryRequestForm(forms.ModelForm):
    name = forms.CharField(max_length=50)

    class Meta:
        model = MediaCategory
        fields = ('name',)

class MediumForm(forms.ModelForm):
    name = forms.CharField(max_length=50,)
    description = forms.CharField(max_length=200,)
    thumbnail = forms.ImageField()

    class Meta:
        model = Medium
        fields = ('name', 'description', 'thumbnail',)
    
                             
        
