from django.urls import path
from .views import AboutView, ArticleDetailView, TopicListView, ArticleListView, CommentCreateView, CommentDeleteView, \
    ArticleCreateView, ArticleUpdateView, Login, Register, Logout
from .views import ArticleDeleteView, subscribe_on_topics, unsubscribe_from_topics, show_profile
from .views import set_password, deactivate

app_name = 'main'

urlpatterns = [
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
    path('profile/<str:username>/',
         show_profile,
         name='show_profile'),
    path('set-password/', set_password, name='set_password'),
    path('deactivate/', deactivate, name='deactivate_profile'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
