from django.contrib.auth.models import User
from django.test import TestCase
from main.models import Article, Comment, Topic


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

    def test_title_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_get_absolute_url(self):
        article = Article.objects.get(id=1)
        self.assertEqual(article.get_absolute_url(), '/1/')

    def test_object_title_returned(self):
        article = Article.objects.get(id=1)
        expected_object_name = f'{article.title}'
        self.assertEqual(str(article), expected_object_name)

    def test_created_is_not_null(self):
        article = Article.objects.get(id=1)
        self.assertIsNotNone(article.created_at)

    def test_updated_is_not_null(self):
        article = Article.objects.get(id=1)
        self.assertIsNotNone(article.updated_at)

    def test_topic_is_not_null(self):
        article = Article.objects.get(id=1)
        self.assertIsNotNone(article.topics.all())
        self.assertEqual(article.topics.count(), 0)

    def test_author_is_user(self):
        article = Article.objects.get(id=1)
        expected_author = User.objects.get(username='test_user')
        self.assertEqual(article.author, expected_author)


class CommentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
                username='test_user',
                email='test_user@gmail.com',
                password='top_secret'
        )
        article = Article.objects.create(title='Test article',
                                         content='Test article content',
                                         author=user)
        Comment.objects.create(message='Test comment',
                               article=article,
                               author=user)

    def test_comment_creation(self):
        comment = Comment.objects.create(
                message='Test Comment',
                article=Article.objects.get(id=1),
                author=User.objects.get(id=1),
                comment=None
        )

        saved_comment = Comment.objects.get(id=comment.id)

        self.assertEqual(saved_comment.message, 'Test Comment')
        self.assertEqual(saved_comment.article, Article.objects.get(id=1))
        self.assertEqual(saved_comment.author, User.objects.get(id=1))
        self.assertIsNone(saved_comment.comment)

    def test_comment_ordering(self):
        comment1 = Comment.objects.create(
                message='Comment 1',
                article=Article.objects.get(id=1),
                author=User.objects.get(id=1),
                comment=None
        )
        comment2 = Comment.objects.create(
                message='Comment 2',
                article=Article.objects.get(id=1),
                author=User.objects.get(id=1),
                comment=None
        )

        ordered_comments = Comment.objects.all()

        self.assertEqual(ordered_comments[0], comment2)
        self.assertEqual(ordered_comments[1], comment1)

    def test_object_message_returned(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f'{comment.message}'
        self.assertEqual(str(comment), expected_object_name)

    def test_message_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('message').max_length
        self.assertEqual(max_length, 400)

    def test_author_is_user(self):
        comment = Comment.objects.get(id=1)
        expected_author = User.objects.get(username='test_user')
        self.assertEqual(comment.author, expected_author)

    def test_article_is_article(self):
        comment = Comment.objects.get(id=1)
        expected_article = Article.objects.get(title='Test article')
        self.assertEqual(comment.article, expected_article)

    def test_created_is_not_null(self):
        comment = Comment.objects.get(id=1)
        self.assertIsNotNone(comment.created_at)


class TopicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Topic.objects.create(
                title='Test Topic',
                description='Test Description')

    def test_title_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('title').max_length
        self.assertEqual(max_length, 64)

    def test_object_name_is_title(self):
        topic = Topic.objects.get(id=1)
        expected_object_name = topic.title
        self.assertEqual(str(topic), expected_object_name)

    def test_description_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)

    def test_subscribers_is_not_null(self):
        topic = Topic.objects.get(id=1)
        self.assertIsNotNone(topic.subscribers)
        self.assertEqual(topic.subscribers.count(), 0)
