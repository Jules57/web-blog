from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Article, Topic


def article_list(request):
    article_list = Article.objects.all()
    # Pagination with 3 articles per page
    paginator = Paginator(article_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    topics = Topic.objects.all()  # Retrieve topics from your model
    return render(request,
                  'main/post/list.html',
                  {
                      'articles': articles,
                      'topics': topics})


def show_about(request):
    return render(request, 'main/about.html')


def article_detail(request, article_id):
    article = get_object_or_404(Article,
                                pk=article_id)
    comments = article.comment_set.all()
    return render(request,
                  'main/post/detail.html',
                  {
                      'article': article,
                      'comments': comments})


def topic_list(request):
    topic_list = Topic.objects.all()
    paginator = Paginator(topic_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        topics = paginator.page(page_number)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request,
                  'main/topic/topic_list.html',
                  {'topics': topics})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic,
                              pk=topic_id)
    articles = topic.articles_on_topic.all()
    return render(request,
                  'main/topic/topic_detail.html',
                  {
                      'topic': topic,
                      'articles': articles})


def add_comment(request, article_id):
    return render(request, 'main/post/add_comment.html')


def create_article(request):
    return render(request, 'main/post/create_article.html')


def update_article(request, article_id):
    return render(request, 'main/post/update_article.html')


def delete_article(request, article_id):
    return render(request, 'main/post/delete_article.html')


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
