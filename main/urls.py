from django.urls import path, include

from .API.urls import router
from .views import AboutView, ArticleDetailView, TopicListView, ArticleListView, CommentCreateView, CommentDeleteView, \
    ArticleCreateView, ArticleUpdateView, Login, Register, Logout, UserDetailView, UserUpdateView
from .views import ArticleDeleteView, subscribe_on_topics, unsubscribe_from_topics
from .views import UserPasswordChangeView, UserDeleteView

app_name = 'main'


urlpatterns = [
    path('api/', include(router.urls)),
    path('', ArticleListView.as_view(), name='home_page'),
    path('about/', AboutView.as_view(), name='about_page'),
    path('<int:article_id>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:article_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('<int:article_id>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('create/', ArticleCreateView.as_view(), name='create_article'),
    path('<int:article_id>/update/',
         ArticleUpdateView.as_view(),
         name='update_article'),
    path('<int:article_id>/delete/',
         ArticleDeleteView.as_view(),
         name='delete_article'),
    path('topics/', TopicListView.as_view(), name='topic_list'),
    path('topics/<int:topic_id>/subscribe/',
         subscribe_on_topics,
         name='subscribe_topic'),
    path('topics/<int:topic_id>/unsubscribe/',
         unsubscribe_from_topics,
         name='unsubscribe_topic'),
    path('profile/<int:pk>/',
         UserDetailView.as_view(),
         name='show_profile'),
    path('profile/<int:pk>/set-userdata/', UserUpdateView.as_view(), name='set_userdata'),
    path('profile/<int:pk>/set-password/', UserPasswordChangeView.as_view(), name='set_password'),
    path('profile/<int:pk>/deactivate/', UserDeleteView.as_view(), name='deactivate_profile'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
