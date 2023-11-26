from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, DeleteView, UpdateView

from .forms import CommentCreateForm, ArticleCreateForm, SearchForm, TopicSubscriptionForm
from .models import Article, Topic, Comment


class Register(CreateView):
    template_name = 'main/user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('main:home_page')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class Login(LoginView):
    template_name = 'main/user/login.html'

    def get_success_url(self):
        return reverse_lazy('main:home_page')


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = reverse_lazy('main:login')


class ArticleListView(ListView):
    template_name = 'main/home.html'
    model = Article
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topic_id = self.request.GET.get('topic_id')
        search_query = self.request.GET.get('search_query')

        articles = Article.objects.all()

        if topic_id:
            context['topic'] = get_object_or_404(Topic, pk=topic_id)
            articles = context['topic'].articles_on_topic.all()

        if search_query:
            articles = articles.filter(title__icontains=search_query)

        context['articles'] = articles
        context['topics'] = Topic.objects.all()
        context['form'] = SearchForm()

        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    pk_url_kwarg = 'article_id'
    template_name = 'main/post/detail.html'
    context_object_name = 'article'
    login_url = reverse_lazy('main:login')
    extra_context = {
        'comment_form': CommentCreateForm()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = Article.objects.get(pk=self.object.pk)
        context['comments'] = article.comments.all()
        return context


class TopicListView(ListView):
    context_object_name = 'topics'
    model = Topic
    template_name = 'main/topic/topic_list.html'
    paginate_by = 6
    extra_context = {'form': TopicSubscriptionForm}


class CommentCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('main:login')
    model = Comment
    pk_url_kwarg = 'article_id'
    form_class = CommentCreateForm
    http_method_names = ['post']

    def get_success_url(self):
        article = self.object.article
        return article.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'article_id': self.kwargs['article_id'],
            'user': self.request.user
        })
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.article = Article.objects.get(pk=form.article_id)
        obj.author = form.user
        obj.message = form.cleaned_data['message']
        obj.save()
        messages.success(self.request, f'Your comment has been successfully added.')
        return super().form_valid(form=form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    login_url = reverse_lazy('main:login')
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        article = self.object.article
        return article.get_absolute_url()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('main:login')
    model = Article
    form_class = ArticleCreateForm
    http_method_names = ['get', 'post']
    template_name = 'main/post/create_article.html'

    def get_success_url(self):
        return reverse_lazy('main:home_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'user': self.request.user
        })
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        # Set the many-to-many relationship for topics
        obj.topics.set(form.cleaned_data['topics'])
        messages.success(self.request, f'Your article has been successfully added.')
        return super().form_valid(form=form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'content', 'topics']
    template_name = 'main/post/update_article.html'
    pk_url_kwarg = 'article_id'
    login_url = reverse_lazy('main:login')


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    login_url = reverse_lazy('main:login')
    pk_url_kwarg = 'article_id'
    template_name = 'main/post/article_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('main:home_page')


class TopicSubscribeView(LoginRequiredMixin, UpdateView):
    # template_name = 'main/topic/topic_subscribe.html'
    login_url = reverse_lazy('main:login')
    model = Topic
    pk_url_kwarg = 'topic_id'
    form_class = TopicSubscriptionForm

    def get_success_url(self):
        return reverse_lazy('main:show_profile', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        topic = form.save(commit=False)
        user = self.request.user
        topic.save()
        topic.subscribers.set([user])
        messages.success(self.request, f'You have successfully subscribed on topic {topic.title}.')
        return super().form_valid(form=form)


class TopicUnsubscribeView(LoginRequiredMixin, UpdateView):
    # template_name = 'main/topic/topic_unsubscribe.html'
    login_url = reverse_lazy('main:login')
    pk_url_kwarg = 'topic_id'
    form_class = TopicSubscriptionForm

    def get_success_url(self):
        return reverse_lazy('main:show_profile', {'pk': self.request.user.pk})

    def form_valid(self, form):
        topic = form.save(commit=False)
        user = self.request.user
        topic.save()
        topic.subscribers.set(user)
        messages.success(self.request, f'You have successfully unsubscribed from topic {topic.title}.')
        return super().form_valid(form=form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'main/user/profile.html'
    context_object_name = 'user'
    login_url = reverse_lazy('main:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.object.pk)
        topics = user.preferred_topics.all()[:3]
        context['topics'] = topics

        articles = user.articles.all()
        context['articles'] = articles

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'main/user/set_userdata.html'
    login_url = reverse_lazy('main:login')

    def get_success_url(self):
        return reverse_lazy('main:show_profile', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/user/set_password.html'
    login_url = reverse_lazy('main:login')

    def get_success_url(self):
        return reverse_lazy('main:show_profile', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the error below.')
        return super().form_invalid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    login_url = reverse_lazy('main:login')
    template_name = 'main/user/confirm_delete.html'
    success_url = reverse_lazy('main:home_page')
