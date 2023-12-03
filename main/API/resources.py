from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from main.API.permissions import IsAuthorOrAdmin, IsProfileOwner, IsAuthorOrReadOnly
from main.API.serializers import TopicSerializer, CommentWriteSerializer, UserSerializer, \
    UserProfileSerializer, UserRegisterSerializer, UserSetPasswordSerializer, CommentReadSerializer, \
    ArticleWriteSerializer, ArticleReadSerializer, TopicSubscriptionSerializer
from main.models import Article, Topic, Comment, UserTokenAuthentication


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return ArticleWriteSerializer
        elif self.request.method == 'GET':
            return ArticleReadSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy', 'partial_update']:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            return CommentWriteSerializer
        elif self.request.method == 'GET':
            return CommentReadSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicSubscriptionAPIView(APIView):
    def post(self, request, topic_id):
        topic = Topic.objects.get(pk=topic_id)
        serializer = TopicSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscribe = serializer.validated_data['subscribe']
        user = request.user

        if subscribe:
            topic.subscribers.add(user)
        else:
            topic.subscribers.remove(user)

        return Response({'success': True}, status=status.HTTP_200_OK)


class LogoutApiView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [UserTokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        elif self.request.method == 'GET' and self.request.query_params.get('profile', '') == 'yes':
            return UserProfileSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'set_password']:
            permission_classes = []
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsProfileOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])
        user = serializer.save(password=password)
        Token.objects.get_or_create(user=user)

    @action(methods=["post"], detail=True)
    def set_password(self, request, pk):
        user = self.get_object()
        if user != request.user:
            return Response({"detail": "You cannot perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSetPasswordSerializer(data=self.request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        Token.objects.filter(user=user).delete()
        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)
