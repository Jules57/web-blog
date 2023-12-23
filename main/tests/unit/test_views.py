from importlib import import_module

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from main.views import Register, Login


class TestRegisterUnit(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch("main.views.login")
    def test_register_success(self, login_mock):
        request = self.factory.post('register/')
        view = Register()
        view.setup(request)
        data = {"username": 'test', "password1": 'TestPass1!', "password2": 'TestPass1!'}
        form = UserCreationForm(data=data)
        form.is_valid()
        view.form_valid(form)
        user = User.objects.first()
        self.assertEquals(user.username, "test")
        self.assertTrue(user.check_password("TestPass1!"))
        self.assertEquals(User.objects.count(), 1)

    def test_register_success_user_in_request(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        request = self.factory.post('register/')
        request.session = store
        request.user = None
        view = Register()
        view.setup(request)
        data = {"username": 'test', "password1": 'TestPass1!', "password2": 'TestPass1!'}
        form = UserCreationForm(data=data)
        form.is_valid()
        view.form_valid(form)
        user = User.objects.first()
        self.assertEquals(request.user, user)

    def test_register_redirect_after_success(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        request = self.factory.post('register/')
        request.session = store
        view = Register()
        view.setup(request)
        data = {"username": 'test', "password1": 'TestPass1!', "password2": 'TestPass1!'}
        form = UserCreationForm(data=data)
        form.is_valid()
        response = view.form_valid(form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_register_failure_duplicate_user(self):
        User.objects.create_user(username='test', password='TestPass1!')
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        request = self.factory.post('register/')
        request.session = store
        view = Register()
        view.setup(request)
        data = {"username": 'test', "password1": 'TestPass1!', "password2": 'TestPass1!'}
        form = UserCreationForm(data=data)
        form.is_valid()
        response = view.form_invalid(form)
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
                username='testuser',
                password='testpassword123')
        self.factory = RequestFactory()
        self.client = Client()
        self.login_url = reverse_lazy('main:login')
        self.home_page_url = reverse_lazy('main:home_page')
        self.create_article = reverse_lazy('main:create_article')

    def test_login_view(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        login_data = {'username': 'testuser', 'password': 'testpassword123'}
        request = self.factory.post('login/', data=login_data)
        request.session = store
        view = Login()
        view.setup(request)
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('main:home_page'))

        user = get_user_model().objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

    def test_login_view_loads_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/user/login.html')

    # def test_login_successful(self):
    #     data = {'username': 'test_user', 'password': 'test_password'}
    #     response = self.client.post(self.login_url, data)
    #     self.assertRedirects(response, self.home_page_url)

    def test_login_unsuccessful(self):
        data = {'username': 'test_user', 'password': 'wrong_password'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/user/login.html')
# integration test
#     def test_unauthenticated_user_redirected(self):
#         # self.client.login(username='test_user', password='test_password')
#         response = self.client.get(self.create_article)
#         self.assertRedirects(response, self.login_url)
