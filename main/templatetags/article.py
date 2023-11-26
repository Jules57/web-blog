from django import template

register = template.Library()


@register.inclusion_tag('main/template_tags/render_article.html')
def render_article(obj):
    title = obj.title
    content = obj.content[:50]
    created = obj.created_at
    topics = ', '.join([topic.title for topic in obj.topics.all()][:3])
    comments = obj.comments.count()
    return {
        'article': obj,
        'title': title,
        'content': content,
        'created_at': created,
        'topics': topics,
        'comments': comments}
