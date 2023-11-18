from importlib import import_module
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, RequestFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from main.views import Register


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


class TestRegisterIntegration(TestCase):

    def test_register_success(self):
        data = {"username": 'test', "password1": 'TestPass1!', "password2": 'TestPass1!'}
        response = self.client.post("/register/", data=data)
        user = User.objects.first()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(user.username, "test")
        self.assertTrue(user.check_password("TestPass1!"))
        self.assertEquals(User.objects.count(), 1)

    def test_register_failed_different_passwords(self):
        data = {"username": 'test', "password1": 'TestPass1!', "password2": 'TestPass2!'}
        response = self.client.post("/register/", data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(User.objects.count(), 0)

    def test_register_failed_invalid_name(self):
        data = {"username": True, "password1": 'TestPass1!', "password2": 'TestPass1!'}
        response = self.client.post("/register/", data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 0)


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_register(self):
        self.selenium.get(f"{self.live_server_url}/register/")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("myuser")
        password_input = self.selenium.find_element(By.NAME, "password1")
        password_input.send_keys("SuperSecret1!")
        password_input2 = self.selenium.find_element(By.NAME, "password2")
        password_input2.send_keys("SuperSecret1!")
        self.selenium.find_element(By.XPATH, '//input[@value="Register"]').click()

