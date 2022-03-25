from django.test import TestCase

from rango.forms import UserForm, UserProfileForm, MediumForm
from django.forms import fields as django_fields

class UserFormTest(TestCase):

    def test_user_form_fields(self):
        form = UserForm()
        fields = form.fields
        expected_fields = {'username':django_fields.CharField, 'email':django_fields.EmailField, 'password':django_fields.CharField}

        for field in expected_fields:
            expected_field = expected_fields[field]
            self.assertTrue(field in fields.keys())
            self.assertEqual(expected_field, type(fields[field]))

    def test_user_form_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields["password"].label is None or form.fields["password"].label == "password")

class UserProfileFormTest(TestCase):

    def test_user_profile_form_fields(self):
        form = UserProfileForm()
        fields = form.fields
        expected_fields = {'picture':django_fields.ImageField}

        for field in expected_fields:
            expected_field = expected_fields[field]
            self.assertTrue(field in fields.keys())
            self.assertEqual(expected_field, type(fields[field]))

class MediumFormTest(TestCase):

    def test_user_profile_form_fields(self):
        form = MediumForm()
        fields = form.fields
        expected_fields = {'name':django_fields.CharField, 'description':django_fields.CharField, 'thumbnail':django_fields.ImageField, }

        for field in expected_fields:
            expected_field = expected_fields[field]
            self.assertTrue(field in fields.keys())
            self.assertEqual(expected_field, type(fields[field]))

    def test_user_form_name_label(self):
        form = MediumForm()
        self.assertTrue(form.fields["name"].label is None or form.fields["name"].label == "name")

    def test_user_form_description_label(self):
        form = MediumForm()
        self.assertTrue(form.fields["description"].label is None or form.fields["description"].label == "description")

    def test_user_form_thumbnail_label(self):
        form = MediumForm()
        self.assertTrue(form.fields["thumbnail"].label is None or form.fields["thumbnail"].label == "thumbnail")

