from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from main.API.permissions import IsAuthorOrReadOnly
from main.API.serializers import ArticleSerializer, TopicSerializer, CommentSerializer, UserSerializer
from main.models import Article, Topic, Comment, UserTokenAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [UserTokenAuthentication]

    # {"username": "mike", "password": "12HappyNewFuckup"}
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = make_password(serializer.validated_data['password'])

            user = User.objects.create(
                    username=serializer.validated_data['username'],
                    password=password
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Добавим действие для выхода (удаления токена)
    @action(detail=False, methods=['post'])
    @permission_classes([IsAuthenticated])
    def logout(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated])
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user)
        articles = user.articles.all()
        article_serializer = ArticleSerializer(articles, many=True)
        topics = user.preferred_topics.all()
        topic_serializer = TopicSerializer(topics, many=True)
        return Response({
            'user': serializer.data,
            'articles': article_serializer.data,
            'topics': topic_serializer.data},
                status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    @permission_classes([IsAuthenticated])
    def set_data(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    @permission_classes([IsAuthenticated])
    def change_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('password')
        if new_password:
            user.set_password(new_password)
            user.save()
            Token.objects.filter(user=user).delete()
            return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'New password not provided.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @permission_classes([IsAuthenticated])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response({'message': 'User successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class CommentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
