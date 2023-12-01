from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import Article, Comment, Topic


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
        fields = ['id', 'message', 'article', 'created_at']
        read_only_fields = ['author']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'token']
        write_only_fields = ['password', 'password2']
        read_only_fields = ['id']

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).count():
            raise ValidationError('This username is already taken.')

        if attrs['password'] != attrs['password2']:
            raise ValidationError('Passwords did not match.')
        attrs.pop('password2')
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, source='preferred_topics')
    articles = ArticleSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'topics', 'articles']


class UserSetPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password2']

    def validate(self, attrs):
        if not self.instance.check_password(attrs['old_password']):
            raise ValidationError("Old password not valid")
        if attrs['new_password'] != attrs['new_password2']:
            raise ValidationError("New passwords are different")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
