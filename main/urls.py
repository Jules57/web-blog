from django.urls import path
from .views import *

urlpatterns = [
    path('', index_page, name='home_page'),
    path('about/', main, name='index_page'),
    path('<int:article_id>/', show_article, name='article'),
    path('<int:article_id>/comment/', add_comment, name='add_comment'),
    path('create/', create_article, name='create_article'),
    path('<int:article_id>/update/', update_article, name='update_article'),
    path('<int:article_id>/delete/', delete_article, name='delete_article'),
    path('topics/', show_topics, name='show_topics'),
    path('topics/<int:topic_id>/subscribe/', subscribe_on_topics, name='subscribe_topic'),
    path('topics/<int:topic_id>/unsubscribe/', unsubscribe_from_topics, name='unsubscribe_topic'),

    path('profile/<str:username>/', show_profile, name='show_profile'),
    path('set-password/', set_password, name='set_password'),
    path('set-userdata/', set_userdata, name='set_userdata'),
    path('deactivate/', deactivate, name='deactivate_profile'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    # path('archive/<int:year>/<int:month>/', show_month_articles, name='monthly'),
]
