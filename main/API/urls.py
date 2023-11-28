from rest_framework import routers

from main.API.resources import ArticleViewSet, TopicViewSet, CommentViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'user', UserViewSet)

urlpatterns = router.urls
