from django.test import TestCase

from django.urls import reverse

from rango.models import Medium, UserEntity, MediaCategory
from django.contrib.auth.models import User

class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = UserEntity.objects.create(name="Author")
        for i in range(5):
            Medium.objects.create(name="Medium" + str(i), medium_author=author)
            UserEntity.objects.create(name="UserEntityTest" + str(i))
            MediaCategory.objects.create(name="MediaCategoryTest" + str(i))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_index_context_dictionary(self):
        self.response = self.client.get(reverse('rango:index'))
        self.assertTrue('posts' in self.response.context)
        self.assertTrue('media_categories' in self.response.context)
        self.assertTrue('users' in self.response.context)

        self.response = self.client.get(reverse('rango:index'))
        contextDict = self.response.context

        expected_medium_order = list(Medium.objects.order_by('-publish_date')[:5])
        self.assertEqual(expected_medium_order, list(contextDict['posts']))

        expected_media_category_order = list(MediaCategory.objects.filter(approved=True).order_by('name'))
        self.assertEqual(expected_media_category_order, list(contextDict['media_categories']))

        expected_user_entity_order = list(UserEntity.objects.order_by('name'))
        self.assertEqual(expected_user_entity_order, list(contextDict['users']))

class AboutViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('rango:about'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rango:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/about.html')

class AddCategoryTest(TestCase):

    def test_add_category_logged_out(self):
        response = self.client.get(reverse('rango:add_category'))
        self.assertEqual(response.status_code, 302)

    def test_add_category_logged_in(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:add_category'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:add_category'))
        self.assertTemplateUsed(response, 'rango/add_category.html')

class RegisterProfileViewTest(TestCase):

    def test_add_category_logged_out(self):
        response = self.client.get(reverse('rango:register_profile'))
        self.assertEqual(response.status_code, 302)

    def test_add_category_logged_in(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:register_profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:register_profile'))
        self.assertTemplateUsed(response, 'rango/profile_registration.html')

class ProfileViewTest(TestCase):

    def test_profile_view_logged_out(self):
        user = create_user_object()
        name = user.username
        response = self.client.get(reverse('rango:profile', kwargs={'username': name}))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_logged_in(self):
        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:profile', kwargs={'username':name}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:profile', kwargs={'username':name}))
        self.assertTemplateUsed(response, 'rango/profile.html')

    def test_profile_view_context_dictionary(self):

        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')
        self.response = self.client.get(reverse('rango:profile', kwargs={'username': name}))

        self.assertTrue('userprofile' in self.response.context)
        self.assertTrue('selecteduser' in self.response.context)
        self.assertTrue('form' in self.response.context)
        self.assertTrue('posts' in self.response.context)
        self.assertTrue('users_list' in self.response.context)

        contextDict = self.response.context

        expected_medium_order = list(Medium.objects.order_by('-publish_date')[:5])
        self.assertEqual(expected_medium_order, list(contextDict['posts']))


def create_user_object():
    user = User.objects.get_or_create(username='testuser', first_name='Test', last_name='User', email='test@test.com')[0]
    user.set_password('123')
    user.save()

    return user
