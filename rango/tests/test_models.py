from django.test import TestCase

from rango.models import UserEntity, MediaCategory, Medium, Review, UserProfile
from django.contrib.auth.models import User


class UserEntityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        UserEntity.objects.create(name="UserEntityTest")

    def test_name_label(self):
        user = UserEntity.objects.get(id=1)
        field_label = user._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        user = UserEntity.objects.get(id=1)
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_profile_picture_label(self):
        user = UserEntity.objects.get(id=1)
        field_label = user._meta.get_field("profile_picture").verbose_name
        self.assertEqual(field_label, "profile picture")

    def test_followed_users_label(self):
        user = UserEntity.objects.get(id=1)
        field_label = user._meta.get_field("followed_users").verbose_name
        field_label
        self.assertEqual(field_label, "followed users")

    def test_user_name(self):
        user = UserEntity.objects.get(id=1)
        userName = user.name
        self.assertEqual(str(user), userName)

class MediaCategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MediaCategory.objects.create(name="MediaCategoryTest")

    def test_name_label(self):
        media = MediaCategory.objects.get(id=1)
        field_label = media._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        media = MediaCategory.objects.get(id=1)
        max_length = media._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_user_name(self):
        media = MediaCategory.objects.get(id=1)
        mediaName = media.name
        self.assertEqual(str(media), mediaName)

class MediumModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = UserEntity.objects.create(name="Author")
        Medium.objects.create(name="MediumTest", medium_author=author, description="Desc test", views=44, likes=10)

    def test_name_label(self):
        medium = Medium.objects.get(id=1)
        field_label = medium._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        medium = Medium.objects.get(id=1)
        max_length = medium._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_thumbnail_label(self):
        medium = Medium.objects.get(id=1)
        description = medium._meta.get_field("description").verbose_name
        self.assertEqual(description, "description")

    def test_publish_date_label(self):
        medium = Medium.objects.get(id=1)
        publish_date = medium._meta.get_field("publish_date").verbose_name
        self.assertEqual(publish_date, "publish date")

    def test_views_label(self):
        medium = Medium.objects.get(id=1)
        views = medium._meta.get_field("views").verbose_name
        self.assertEqual(views, "views")

    def test_likes_label(self):
        medium = Medium.objects.get(id=1)
        likes = medium._meta.get_field("likes").verbose_name
        self.assertEqual(likes, "likes")

    def test_medium_author_label(self):
        medium = Medium.objects.get(id=1)
        medium_author = medium._meta.get_field("medium_author").verbose_name
        self.assertEqual(medium_author, "medium author")

    def test_likes_label(self):
        medium = Medium.objects.get(id=1)
        medium_category = medium._meta.get_field("medium_category").verbose_name
        self.assertEqual(medium_category, "medium category")

    def test_medium_name(self):
        medium = Medium.objects.get(id=1)
        mediumName = medium.name
        self.assertEqual(str(medium), mediumName)

    def test_medium_description(self):
        medium = Medium.objects.get(id=1)
        mediumDescription = medium.description
        self.assertEqual("Desc test", mediumDescription)

    def test_medium_views(self):
        medium = Medium.objects.get(id=1)
        mediumViews = medium.views
        self.assertEqual(44, mediumViews)

    def test_medium_likes(self):
        medium = Medium.objects.get(id=1)
        mediumLikes = medium.likes
        self.assertEqual(10, mediumLikes)


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = UserEntity.objects.create(name="Author")
        mediumAuthor = UserEntity.objects.create(name="Medium Author")
        medium = Medium.objects.create(name="Media", medium_author=mediumAuthor)
        Review.objects.create(text="ReviewTest", reviewed_medium=medium, review_author=author, likes=24)

    def test_text_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field("text").verbose_name
        self.assertEqual(field_label, "text")

    def test_upload_date_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field("upload_date").verbose_name
        self.assertEqual(field_label, "upload date")

    def test_likes_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field("likes").verbose_name
        self.assertEqual(field_label, "likes")

    def test_reviewed_medium_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field("reviewed_medium").verbose_name
        self.assertEqual(field_label, "reviewed medium")

    def test_review_author_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field("review_author").verbose_name
        self.assertEqual(field_label, "review author")

    def test_review_name(self):
        review = Review.objects.get(id=1)
        reviewText = review.text
        self.assertEqual(str(review), reviewText)

    def test_medium_likes(self):
        review = Review.objects.get(id=1)
        reviewLikes = review.likes
        self.assertEqual(24, reviewLikes)

class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Test User", password="123")
        UserProfile.objects.create(user=user)

    def test_user_label(self):
        userProfile = UserProfile.objects.get(id=1)
        field_label = userProfile._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_user_profile_name(self):
        userProfile = UserProfile.objects.get(id=1)
        field_label = userProfile.user.username
        self.assertEqual(str(userProfile), field_label)

