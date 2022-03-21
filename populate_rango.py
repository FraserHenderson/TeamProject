import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, UserEntity, Medium, MediaCategory, Review

from datetime import datetime
from django.core.files import File
from django.conf import settings

def populate():

    users = [
        {'name': 'Matas',
        'profile_picture': None,
        'login_status': False,
        'followed_users': []},
        {'name': 'Matt',
        'profile_picture': None,
        'login_status': False,
        'followed_users': ['Matas']},
        {'name': 'Matthew',
        'profile_picture': None,
        'login_status': False,
        'followed_users': ['Matas']},
    ]

    categories = [
        {'name': 'Flower'},
        {'name': 'Landscape'},
        {'name': 'Rodent'},
        {'name': 'Cat'},
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
        'description': 'Say ü',
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

    # Old stuff
    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/',
        'views':1},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/',
        'views':10},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/',
        'views':11} ]

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'views':12},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'views':17},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'views':22} ]

    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/',
        'views':5},
        {'title':'Flask',
        'url':'http://flask.pocoo.org',
        'views':8} ]

    cats = {'Python': {'pages': [python_pages,128,64]},
        'Django': {'pages': [django_pages,64,32]},
        'Other Frameworks': {'pages': [other_pages,32,16]} }
    # Old stuff


    # Old stuff
    for cat, cat_data in cats.items():
        c = add_cat(cat,views=cat_data['pages'][1],likes=cat_data['pages'][2])
        for p in cat_data['pages'][0]:
            add_page(c,p['title'], p['url'], views=p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
    # Old stuff

    for user_data in users:
        add_user(name=user_data['name'], profile_picture=user_data['profile_picture'], login_status=user_data['login_status'], followed_users=user_data['followed_users'])

    for category_data in categories:
        add_category(name=category_data['name'])

    for medium_data in media:
        add_medium(name=medium_data['name'], description=medium_data['description'], thumbnail=medium_data['thumbnail'], publish_date=medium_data['publish_date'], views=medium_data['views'], likes=medium_data['likes'], medium_author=medium_data['medium_author'], medium_category=medium_data['medium_category'])
    
    for review_data in reviews:
        add_review(text=review_data['text'], upload_date=review_data['upload_date'], likes=review_data['likes'], reviewed_medium=review_data['reviewed_medium'], review_author=review_data['review_author'])



# Old stuff
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.views = views
    c.save()
    return c
# Old stuff




def add_user(name, profile_picture=None, login_status=False, followed_users=[]):
    u = UserEntity.objects.get_or_create(name=name)[0]
    u.name = name
    u.profile_picture = profile_picture
    u.login_status = login_status

    # Does not work
    # for fu in followed_users:
    #     if fu not in u.followed_users:
    #         u.followed_users.add(fu)

    u.save()
    return u

def add_category(name):
    c = MediaCategory.objects.get_or_create(name=name)[0]
    c.name = name
    c.save()
    return c

def add_medium(name, medium_author, medium_category, description='', thumbnail=None, publish_date=datetime.now(), views=0, likes=0):
    author = UserEntity.objects.get(name=medium_author)
    category = MediaCategory.objects.get(name=medium_category)

    m = Medium.objects.get_or_create(name=name, medium_author=author, medium_category=category)[0]
    m.name = name
    m.description = description
    #m.thumbnail = thumbnail
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
    
            
