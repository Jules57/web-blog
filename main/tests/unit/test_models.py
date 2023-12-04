from django.contrib.auth.models import User
from django.test import TestCase
from main.models import Article


class ArticleTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
                username='test_user',
                email='test_user@gmail.com',
                password='top_secret'
        )
        Article.objects.create(title='Test article',
                               content='Test article content',
                               author=user)

    def test_first_name_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_get_absolute_url(self):
        article = Article.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(article.get_absolute_url(), '/1/')

    def test_object_title_returned(self):
        article = Article.objects.get(id=1)
        expected_object_name = f'{article.title}'
        self.assertEqual(str(article), expected_object_name)
