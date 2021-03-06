import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import UserEntity, Medium, MediaCategory, Review

from datetime import datetime
from django.core.files import File
from django.conf import settings

def populate():

    users = [
        {'name': 'Matas',
        'profile_picture': 'Blue_rook.jpg',
        'followed_users': []},
        {'name': 'Matt',
        'profile_picture': 'White_horse.png',
        'followed_users': ['Matas']},
        {'name': 'Matthew',
        'profile_picture': 'Red_pawn.jpg',
        'followed_users': ['Matas']},
    ]

    categories = [
        {'name': 'Flower',
        'approved': True},
        {'name': 'Landscape',
        'approved': True},
        {'name': 'Rodent',
        'approved': False},
        {'name': 'Cat',
        'approved': True},
    ]

    media = [
        {'name': 'Squirrel',
        'description': 'A cute squirrel from the Kelvingrove Park',
        'thumbnail': 'Squirrel.jpg',
        'publish_date': datetime(2022, 2, 24, 15, 34, 56),
        'views': 45,
        'likes': 13,
        'medium_author': 'Matas',
        'medium_category': 'Rodent'},

        {'name': 'Lotus',
        'description': 'Lotus',
        'thumbnail': 'Lotus.jpg',
        'publish_date': datetime(2022, 1, 24, 14, 54, 56),
        'views': 13,
        'likes': 4,
        'medium_author': 'Matas',
        'medium_category': 'Flower'},

        {'name': 'Field of roses',
        'description': 'A truly awe-inspiring field of beauty',
        'thumbnail': 'Field_of_roses.jpg',
        'publish_date': datetime(2022, 1, 16, 7, 15, 47),
        'views': 35,
        'likes': 12,
        'medium_author': 'Matt',
        'medium_category': 'Flower'},

        {'name': 'Daffodils',
        'description': 'I have grown these!',
        'thumbnail': 'Daffodils.jpg',
        'publish_date': datetime(2022, 2, 28, 2, 54, 13),
        'views': 3,
        'likes': 0,
        'medium_author': 'Matt',
        'medium_category': 'Flower'},

        {'name': 'Wierd Cat',
        'description': 'Say ??',
        'thumbnail': 'Wierd_cat.jpg',
        'publish_date': datetime(2022, 3, 20, 16, 34, 46),
        'views': 7,
        'likes': 3,
        'medium_author': 'Matt',
        'medium_category': 'Cat'},
    ]

    reviews = [
        {'text': 'Such a cute squirrel! <3',
        'upload_date': datetime(2022, 3, 5, 14, 32, 45),
        'likes': 2,
        'reviewed_medium': 'Squirrel',
        'review_author': 'Matt'},

        {'text': 'There are much prettier flowers...',
        'upload_date': datetime(2022, 3, 13, 23, 36, 24),
        'likes': 5,
        'reviewed_medium': 'Daffodils',
        'review_author': 'Matas'},
    ]

   

    for user_data in users:
        add_user(name=user_data['name'], profile_picture=user_data['profile_picture'], followed_users=user_data['followed_users'])

    for category_data in categories:
        add_category(name=category_data['name'], approved=category_data['approved'])

    for medium_data in media:
        add_medium(name=medium_data['name'], description=medium_data['description'], thumbnail=medium_data['thumbnail'], publish_date=medium_data['publish_date'], views=medium_data['views'], likes=medium_data['likes'], medium_author=medium_data['medium_author'], medium_category=medium_data['medium_category'])
    
    for review_data in reviews:
        add_review(text=review_data['text'], upload_date=review_data['upload_date'], likes=review_data['likes'], reviewed_medium=review_data['reviewed_medium'], review_author=review_data['review_author'])




def add_user(name, profile_picture='Default_profile_picture.jpg', followed_users=[]):
    u = UserEntity.objects.get_or_create(name=name)[0]
    u.name = name
    u.profile_picture.save('profile_picture.png', File(open(os.path.join(settings.MEDIA_DIR, profile_picture), 'rb')))

    # Does not work
    # for fu in followed_users:
    #     if fu not in u.followed_users:
    #         u.followed_users.add(fu)

    u.save()
    return u

def add_category(name, approved=False):
    c = MediaCategory.objects.get_or_create(name=name)[0]
    c.name = name
    c.approved = approved
    c.save()
    return c

def add_medium(name, medium_author, medium_category, description='', thumbnail=None, publish_date=datetime.now(), views=0, likes=0):
    author = UserEntity.objects.get(name=medium_author)
    category = MediaCategory.objects.get(name=medium_category)

    m = Medium.objects.get_or_create(name=name, medium_author=author, medium_category=category)[0]
    m.name = name
    m.description = description
    m.publish_date = datetime.strptime((str(publish_date))[:19], '%Y-%m-%d %H:%M:%S')
    # Uploading files from file system taken from: https://stackoverflow.com/questions/15332086/saving-image-file-through-django-shell
    m.thumbnail.save('thumbnail.png', File(open(os.path.join(settings.MEDIA_DIR, thumbnail), 'rb')))
    m.views = views
    m.likes = likes
    m.save()
    return m

def add_review(text, reviewed_medium, review_author, upload_date=datetime.now(), likes=0):
    author = UserEntity.objects.get(name=review_author)
    medium = Medium.objects.get(name=reviewed_medium)

    t = Review.objects.get_or_create(text=text, review_author=author, reviewed_medium=medium)[0]
    t.text = text
    t.upload_date = upload_date
    t.likes = likes
    t.save()
    return t

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
    
            
