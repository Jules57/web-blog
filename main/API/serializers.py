from django.contrib.auth.models import User
from rest_framework import serializers
from main.models import Article, Comment, Topic


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'subscribers']


class ArticleSerializer(serializers.ModelSerializer):
    topics = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'topics']
        read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'message', 'article', 'created_at', 'author']
