from django.contrib import admin
from rango.models import UserEntity, Medium, MediaCategory, Review
from rango.models import UserProfile


# Register your models here.

admin.site.register(UserEntity)
admin.site.register(Medium)
admin.site.register(MediaCategory)
admin.site.register(Review)

# Old registers
admin.site.register(UserProfile)