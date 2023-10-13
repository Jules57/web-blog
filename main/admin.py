from django.contrib import admin
from .models import Article, Comment, Topic


# admin.site.register(Article)
# admin.site.register(Topic)
# admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['author', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'message', 'created_at']
    list_filter = ['author', 'created_at']
    search_fields = ['author', 'created_at']
