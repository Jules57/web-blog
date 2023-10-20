from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import AuthenticationForm, RegisterForm, CommentCreateForm, ArticleCreateForm, SearchForm
from .models import Article, Topic, Comment


def home_page(request):
    if request.method == 'GET':
        topic_id = request.GET.get('topic_id')
        search_query = request.GET.get('search_query')

        if topic_id:
            topic = Topic.objects.get(pk=topic_id)
            articles = topic.articles_on_topic.all()
            return render(request,
                          'main/home.html',
                          {
                              'articles': articles,
                              'topic': topic})

        if search_query:
            articles = Article.objects.filter(title__icontains=search_query)
            return render(request,
                          'main/home.html',
                          {'articles': articles})
        else:
            articles = Article.objects.all()
            topics = Topic.objects.all()
            form = SearchForm()
            return render(request,
                          'main/home.html', {
                              'form': form,
                              'articles': articles,
                              'topics': topics})


def show_about(request):
    return render(request, 'main/about.html')


@login_required(login_url='/login/')
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.all()
    return render(request,
                  'main/post/detail.html',
                  {
                      'article': article,
                      'comments': comments})


def topic_list(request):
    topics = Topic.objects.all()
    return render(request,
                  'main/topic/topic_list.html',
                  {'topics': topics})


@login_required(login_url='/login/')
def add_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            # Save the comment with the associated article and author
            author = request.user
            message = comment_form.cleaned_data['message']
            Comment.objects.create(message=message, author=author, article=article)
            return redirect(reverse('main:article_detail', args=[article_id]))
    else:
        comment_form = CommentCreateForm()
        return render(request,
                      'main/post/add_comment.html',
                      {
                          'article': article,
                          'comment_form': comment_form})


@login_required(login_url='/login/')
def create_article(request):
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            # Create and save the article
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            topics = form.cleaned_data['topics']
            author = request.user
            created_at = timezone.now()
            new_article = Article(title=title, content=content, author=author, created_at=created_at)
            new_article.save()

            # Add the selected topics to the new article
            new_article.topics.set(topics)
            return redirect(reverse('main:home_page'))

    else:
        form = ArticleCreateForm()
        return render(request, 'main/post/create_article.html', {'form': form})
    return render(request, 'main/post/create_article.html')


@login_required(login_url='/login/')
def update_article(request, article_id):
    return render(request, 'main/post/update_article.html')


@login_required(login_url='/login/')
def delete_article(request, article_id):
    return render(request, 'main/post/delete_article.html')


def subscribe_on_topics(request, topic_id):
    return render(request, 'main/topic/topic_subscribe.html')


def unsubscribe_from_topics(request, topic_id):
    return render(request, 'main/topic/topic_unsubscribe.html')


@login_required(login_url='/login/')
def show_profile(request, username):
    return render(request, 'main/user/profile.html', {'username': username})


@login_required(login_url='/login/')
def set_password(request):
    return render(request, 'main/user/set_password.html')


def deactivate(request):
    return render(request, 'main/user/deactivate.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return reverse('main:home_page')
        messages.error(request, 'Unsuccessful registration. Invalid data.')
    form = RegisterForm()
    return render(request, 'main/user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm()
        return render(request, 'main/user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('main:home_page'))
