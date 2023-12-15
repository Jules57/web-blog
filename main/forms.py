from django import forms

from main.models import Topic, Comment, Article


class ArticleCreateForm(forms.ModelForm):
    topics = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            queryset=Topic.objects.all(),
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'topics']

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        self.user = kwargs.pop('user', None)
        super(ArticleCreateForm, self).__init__(*args, **kwargs)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message', 'article']
        widgets = {
            "article": forms.HiddenInput()
        }


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, label='Search', widget=forms.TextInput)


class TopicSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = []
