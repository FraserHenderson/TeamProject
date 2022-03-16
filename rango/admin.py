from django.contrib import admin
from rango.models import Category, Page, UserEntity, Medium, MediaCategory, Review
from rango.models import UserProfile

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category','url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


# Register your models here.

admin.site.register(UserEntity)
admin.site.register(Medium)
admin.site.register(MediaCategory)
admin.site.register(Review)

# Old registers
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)