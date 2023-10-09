from django.http import HttpResponse
from django.shortcuts import render


def index_page(request):
    return render(request, 'main/post/list.html')


def show_about(request):
    return render(request, 'main/about.html')


def show_article(request, article_id):
    return render(request, 'main/post/detail.html')


def add_comment(request, article_id):
    return render(request, 'main/post/add_comment.html')


def create_article(request):
    return render(request, 'main/post/create_article.html')


def update_article(request, article_id):
    return render(request, 'main/post/update_article.html')


def delete_article(request, article_id):
    return render(request, 'main/post/delete_article.html')


def show_topics(request):
    return render(request, 'main/topic/topic_list.html')


def subscribe_on_topics(request, topic_id):
    return render(request, 'main/topic/topic_subscribe.html')


def unsubscribe_from_topics(request, topic_id):
    return render(request, 'main/topic/topic_unsubscribe.html')


def show_profile(request, username):
    return render(request, 'main/user/profile.html', context={username: 'username'})


def set_password(request):
    return render(request, 'main/user/set_password.html')


def deactivate(request):
    return render(request, 'main/user/deactivate.html')


def register(request):
    return render(request, 'main/user/register.html')


def login(request):
    return render(request, 'main/user/login.html')


def logout(request):
    return render(request, 'main/user/logout.html')
