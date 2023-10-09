from django.urls import path
from .views import index_page, show_article, add_comment, create_article, update_article, show_about
from .views import delete_article, show_topics, subscribe_on_topics, unsubscribe_from_topics, show_profile
from .views import set_password, deactivate, register, login, logout

urlpatterns = [
    path('', index_page, name='home_page'),
    path('about/', show_about, name='index_page'),
    path('<int:article_id>/', show_article, name='article_detail'),
    path('<int:article_id>/comment/', add_comment, name='add_comment'),
    path('create/', create_article, name='create_article'),
    path('<int:article_id>/update/',
         update_article,
         name='update_article'),
    path('<int:article_id>/delete/',
         delete_article,
         name='delete_article'),
    path('topics/', show_topics, name='show_topics'),
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
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
