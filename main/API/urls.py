from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from main.API.resources import ArticleViewSet, TopicViewSet, CommentViewSet, UserViewSet, LogoutApiView

router = routers.SimpleRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls

urlpatterns = [
    # path('articles/{article_id}/comment/', CommentViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    #     'delete': 'destroy'})),
    path('', include(router.urls)),
    path('login/', obtain_auth_token),
    path('logout/', LogoutApiView.as_view()),

]
