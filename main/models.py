from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    topics = models.ManyToManyField('Topic', related_name='articles_on_topic')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:article_detail',
                       args=[str(self.pk)])


class Topic(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(User, related_name='preferred_topics', through='Preference')

    def __str__(self):
        return f'{self.title} with ID {self.pk}'

    def get_absolute_url(self):
        return reverse('main:topic_detail',
                       args=[str(self.pk)])


class Preference(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    notification = models.BooleanField(default=False)


class Comment(models.Model):
    message = models.CharField(max_length=400)
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments')
    comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING,
                                related_name='comments')

    def __str__(self):
        return self.message
