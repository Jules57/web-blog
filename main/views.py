from django.shortcuts import render
from django.http import HttpResponse


def main(request):
    return HttpResponse('Hey! It\'s your main view!')


def index_page(request):
    return HttpResponse('Hey! It\'s your main view!')


def show_article(request, article_id):
    return HttpResponse(f'Single article.')


def add_comment(request, article_id):
    return HttpResponse(f'Leave a comment to article {article_id}.')


def create_article(request):
    return HttpResponse('Create article')


def update_article(request, article_id):
    return HttpResponse(f'Update article {article_id}')


def delete_article(request, article_id):
    return HttpResponse(f'Delete article {article_id}')


def show_topics(request):
    return HttpResponse('Show topics')


def subscribe_on_topics(request, topic_id):
    return HttpResponse(f'Subscribe on topic {topic_id}')


def unsubscribe_from_topics(request, topic_id):
    return HttpResponse(f'Unsubscribe from topic {topic_id}')


def show_profile(request, username):
    return HttpResponse(f'Hello, {username.capitalize()}')


def set_password(request):
    return HttpResponse(f'Set your password')


def set_userdata(request):
    return HttpResponse(f'Set your data')


def deactivate(request):
    return HttpResponse(f'Deactivate your account')


def register(request):
    return HttpResponse(f'Register your account')


def login(request):
    return HttpResponse(f'Login')


def logout(request):
    return HttpResponse(f'Logout')
