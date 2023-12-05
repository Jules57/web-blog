from django import forms
from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Article, Topic
from main.forms import ArticleCreateForm, CommentCreateForm, SearchForm, TopicSubscriptionForm


class ArticleCreateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='test_user1',
                password='testpassword')

        self.topic1 = Topic.objects.create(title='Topic 1')
        self.topic2 = Topic.objects.create(title='Topic 2')
        self.topic3 = Topic.objects.create(title='Topic 3')

    def test_form_valid_data(self):
        form_data = {
            'title': 'Test Article',
            'content': 'Lorem ipsum dolor sit amet.',
            'topics': [self.topic1.id, self.topic2.id],
        }

        form = ArticleCreateForm(data=form_data, user=self.user)

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'content': 'Lorem ipsum dolor sit amet.',
            'topics': [self.topic1.id, self.topic2.id],
        }

        form = ArticleCreateForm(data=form_data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_topics_queryset(self):
        form = ArticleCreateForm(user=self.user)

        self.assertQuerysetEqual(
                form.fields['topics'].queryset,
                Topic.objects.all(),
                ordered=False
        )


class CommentCreateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='testuser',
                password='testpassword')

        self.article = Article.objects.create(
                title='Test Article',
                content='Lorem ipsum dolor sit amet.',
                author=self.user
        )

    def test_form_valid_data(self):
        form_data = {
            'message': 'Test Comment',
            'article': self.article.id,
        }

        form = CommentCreateForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'article': self.article.id,
        }

        form = CommentCreateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_hidden_input_widget(self):
        form = CommentCreateForm()

        self.assertIsInstance(form.fields['article'].widget, forms.HiddenInput)

    def test_hidden_input_widget_rendering(self):
        form = CommentCreateForm()

        widget_html = form.fields['article'].widget.render('article', 'test_value')

        self.assertIn('type="hidden"', widget_html)
        self.assertIn('value="test_value"', widget_html)


class SearchFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'search_query': 'Django'}

        form = SearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_blank_search_query(self):
        form_data = {'search_query': ''}

        form = SearchForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('search_query', form.errors)

    def test_long_search_query(self):
        form_data = {'search_query': 'a' * 101}

        form = SearchForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('search_query', form.errors)

    def test_form_widget(self):
        form = SearchForm()

        self.assertIsInstance(form.fields['search_query'].widget, forms.TextInput)


class TopicSubscriptionFormTest(TestCase):
    def test_form_valid(self):
        topic = Topic.objects.create(title='Test Topic')

        form = TopicSubscriptionForm(instance=topic)

        self.assertFalse(form.is_valid())

    def test_form_save(self):
        topic = Topic.objects.create(title='Test Topic')

        form_data = {'some_extra_data': 'value'}
        form = TopicSubscriptionForm(instance=topic, data=form_data)

        form.save()

        topic.refresh_from_db()
        self.assertEqual(topic.title, 'Test Topic')
