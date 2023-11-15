from rest_framework import serializers
from main.models import Article, Comment, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'description']


class ArticleSerializer(serializers.ModelSerializer):
    topics = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'topics']


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'message', 'article', 'created_at', 'author']