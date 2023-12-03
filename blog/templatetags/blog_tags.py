from django import template
from ..models import Post, Product, Recipe
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def total_products():
    return Product.objects.count()


@register.inclusion_tag('list.html')
def show_recent_products(count=10):
    recent_products = Product.objects.order_by('-publish')[:count]
    return {'recent_products': recent_products}


@register.simple_tag
def total_recipes():
    return Recipe.objects.count()


@register.inclusion_tag('recipe_detail.html')
def show_latest_recipes(count=5):
    latest_recipes = Recipe.objects.order_by('created_by')[:count]
    return {'latest_recipes': latest_recipes}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
