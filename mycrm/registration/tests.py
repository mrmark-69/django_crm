from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase


class SigninTest(TestCase):
    def setUp(self):
        # Создаю пользователя для прохождения теста.
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')

    def tearDown(self):
        self.user.delete()  # Удаляю пользователя после прохождения теста.

    def test_is_authenticated(self):
        # Проверяю что пользователь прошел аутентификацию.
        user = authenticate(username='test', password='12test12')
        self.assertTrue(user is not None and user.is_authenticated)

    def test_wrong_username(self):
        # Проверяю что пользователь ввел неверный логин.
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        # Проверяю что пользователь ввел неверный пароль.
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
