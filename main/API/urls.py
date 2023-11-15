from rest_framework import routers

from main.API.resources import ArticleViewSet, TopicViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
