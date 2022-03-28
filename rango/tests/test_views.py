from django.test import TestCase

from django.urls import reverse

from rango.models import Medium, UserEntity, MediaCategory
from django.contrib.auth.models import User

class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            media = MediaCategory.objects.create(name="test media" + str(i), approved=True)
            user = create_user_object()
            user.username = "test user " + str(i)
            user.email = "test" + str(i) + "test.com"
            author = UserEntity.objects.create(name=user.username)
            Medium.objects.create(name="test medium" + str(i), medium_author=author, medium_category=media)

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

class AddCategoryRequestViewTest(TestCase):

    def test_add_category_logged_out(self):
        user = create_user_object()
        name = user.username
        response = self.client.get(reverse('rango:add_category',kwargs={'username':name}))
        self.assertEqual(response.status_code, 302)

    def test_add_category_logged_in(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:add_category',kwargs={'username':name}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:add_category',kwargs={'username':name}))
        self.assertTemplateUsed(response, 'rango/add_category.html')

    def test_requesting_invalid_category(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')

        response = self.client.post(reverse('rango:add_category', kwargs={'username': name}))
        requests = MediaCategory.objects.filter(approved=False)
        self.assertEqual(len(requests), 0)

    def test_requesting_valid_category(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        data = {'name':'test request'}
        response = self.client.post(reverse('rango:add_category', kwargs={'username':name}), data)
        requests = MediaCategory.objects.filter(approved=False)
        self.assertEqual(len(requests), 1)
        self.assertRedirects(response, '/rango/')

class ShowCategoryRequestsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            MediaCategory.objects.create(name="Test request" + str(i), approved=False)

    def test_show_category_requests_logged_out(self):
        user = create_user_object()
        name = user.username
        response = self.client.get(reverse('rango:view_category_requests',kwargs={'username':name}))
        self.assertEqual(response.status_code, 302)

    def test_show_category_requests_logged_in(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:view_category_requests',kwargs={'username':name}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:view_category_requests',kwargs={'username':name}))
        self.assertTemplateUsed(response, 'rango/category_requests.html')

    def test_show_category_context_dictionary(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:view_category_requests', kwargs={'username': name}))
        test_pending_categories_list = list(MediaCategory.objects.filter(approved=False).order_by('name'))
        self.assertEqual(test_pending_categories_list, list(response.context['pending_categories']))

    def test_approving_category(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        self.assertFalse(MediaCategory.objects.get(name="Test request1").approved)
        response = self.client.post(reverse('rango:view_category_requests', kwargs={'username': name}),{'dropdown':MediaCategory.objects.get(name="Test request1").name})
        self.assertTrue(MediaCategory.objects.get(name="Test request1").approved)




class RegisterProfileViewTest(TestCase):

    def test_register_profile_logged_out(self):
        response = self.client.get(reverse('rango:register_profile'))
        self.assertEqual(response.status_code, 302)

    def test_register_profile_logged_in(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:register_profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:register_profile'))
        self.assertTemplateUsed(response, 'rango/profile_registration.html')

    def test_registration_with_default_picture(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.post(reverse('rango:register_profile'))
        user = list(UserEntity.objects.all())[0]
        self.assertEqual('Default_profile_picture.jpg', user.profile_picture)
        self.assertRedirects(response, '/rango/')

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
        self.assertEqual(response.context['selecteduser'].username, name)

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

    def test_accessing_non_existent_profile(self):
        create_user_object()
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:profile', kwargs={'username': 'wrong'}))
        self.assertRedirects(response, '/rango/')


"""

    def test_proflie_view_post(self):
        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')
        response = self.client.post(reverse('rango:profile', kwargs={'username': name}))
        
"""



class MediumViewTest(TestCase):

    def test_medium_view_logged_out(self):
        user = create_user_object()
        name = user.username
        response = self.client.get(reverse('rango:new_post', kwargs={'username': name}))
        self.assertEqual(response.status_code, 302)

    def test_medium_view_logged_in(self):
        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:new_post', kwargs={'username': name}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:new_post', kwargs={'username': name}))
        self.assertTemplateUsed(response, 'rango/new_post.html')

    def test_medium_view_context_dictionary(self):
        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')
        self.response = self.client.get(reverse('rango:new_post', kwargs={'username': name}))

        self.assertTrue('form' in self.response.context)
        self.assertTrue('user' in self.response.context)
        self.assertTrue('category_list' in self.response.context)
        self.assertTrue('users' in self.response.context)



# Having trouble with thumbnail field, cant mock it

"""
    def test_adding_post(self):
        user = create_user_object()
        name = user.username
        self.client.login(username="testuser", password='123')

        test_author = UserEntity.objects.create(name="Author")

        data = {'name': 'test post',
                'description': 'test description',
                'views': 10,
                'likes': 5,
                'medium_author': test_author}

        self.client.post(reverse('rango:new_post', kwargs={'username': name}), data=data)
        posts = Medium.objects.filter(name='test post')
        self.assertEqual(len(posts),1)
        
"""

class MyCollectionViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:my_collection', kwargs={'username': name}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = create_user_object()
        name = user.username
        UserEntity.objects.create(name=name)
        self.client.login(username="testuser", password='123')
        response = self.client.get(reverse('rango:my_collection', kwargs={'username': name}))
        self.assertTemplateUsed(response, 'rango/my_collection.html')

class SearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            author = UserEntity.objects.create(name="Author " + str(i))
            Medium.objects.create(name="Test medium by author " + str(i), medium_author=author)
            MediaCategory.objects.create(name="Test Media" + str(i))
            user = create_user_object()
            user.username = "User" + str(i)
            user.email = "test" + str(i) + "@test.com"
            UserEntity.objects.create(name=user.username)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('rango:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_with_query(self):

        for medium in Medium.objects.all():
            data = {'query': medium.name}
            response = self.client.post(reverse('rango:search'), data)
            self.assertTrue(medium.name in response.context['query'])

        for user in UserEntity.objects.all():
            data = {'query':user.name}
            response = self.client.post(reverse('rango:search'), data)
            self.assertTrue(user.name in response.context['query'])

        for media in MediaCategory.objects.all():
            data = {'query':media.name}
            response = self.client.post(reverse('rango:search'), data)
            self.assertTrue(media.name in response.context['query'])

class MediaCategoryViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        media = MediaCategory.objects.create(name="test category", approved=True)
        user = create_user_object()
        author = UserEntity.objects.create(name=user.username)
        for i in range(10):
            Medium.objects.create(name="test medium" + str(i), medium_author=author, medium_category=media)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('rango:category', kwargs={'category': "test category"}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rango:category', kwargs={'category': "test category"}))
        self.assertTemplateUsed(response, 'rango/category.html')

    def test_media_category_view_context_dictionary(self):
        response = self.client.get(reverse('rango:category', kwargs={'category': "test category"}))
        self.assertEqual(response.status_code, 200)
        media = MediaCategory.objects.get(name="test category")
        test_posts_list = Medium.objects.filter(medium_category=media).order_by('-publish_date')
        self.assertTrue(response.context['target_category'] == media)
        self.assertTrue(list(response.context['posts']) == list(test_posts_list))

def create_user_object():
    user = User.objects.get_or_create(username='testuser', first_name='Test', last_name='User', email='test@test.com')[0]
    user.set_password('123')
    user.save()

    return user