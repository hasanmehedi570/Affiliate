

from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Product, Recipe, ReCategory
from .forms import CommentForm, RecipeCommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.db.models import Count
from django.db.models import Q
from django.views import generic
from urllib.parse import quote_plus
import random
from django.shortcuts import render
from django.core.cache import cache
from time import sleep
from django.views.decorators.http import require_POST


def time_consuming_task():
    # Simulating a time-consuming task by generating a random number between 1 and 100
    sleep(5)
    return random.randint(1, 100)


def home(request, count=10):
    post1 = Post.published.filter(post_1=True)
    post2 = Post.published.filter(post_2=True)
    post3 = Post.published.filter(post_3=True)
    post4 = Post.published.filter(post_4=True)
    post5 = Post.published.filter(post_5=True)
    products = Product.objects.filter(featured=True)
    recent_products = Product.objects.order_by('-created')[:count]
    categories = Category.objects.all().annotate(products_count=Count('products'))
    return render(request,
                  'home.html',
                  {'post1': post1,
                   'post2': post2,
                   'post3': post3,
                   'post4': post4,
                   'post5': post5,
                   'products': products,
                   'recent_products': recent_products,
                   'categories': categories})


def blog_view(request, tag_slug=None):
    post_list = Post.published.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/post_list.html',
                  {'posts': posts,
                   'post_list': post_list,
                   'products': products,
                   'categories': categories,
                   'tag': tag})


def single_post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post,
                             publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    products = Product.objects.all()
    categories = Category.objects.all()
    posts = Post.published.exclude(id=post.id)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('same_tags', 'publish')[:3]

    result = cache.get('post')
    print("FROM CACHE")
    if result is None:
        print("FROM DATABASE")
        # If not in cache, perform the time-consuming task and store the result in cache
        result = time_consuming_task()
        # Cache result for 30 seconds
        cache.set('post', result, timeout=30)
    return render(request,
                  'posts/post_detail.html',
                  {'post': post,
                   'posts': posts,
                   'products': products,
                   'categories': categories,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


def product_list(request, category_slug=None, tag_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    tag = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        # Pagination with 3 posts per page
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request,
                  'products/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'tag': tag})


def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    product_tags_ids = product.tags.values_list('id', flat=True)
    similar_products = Product.objects.filter(tags__in=product_tags_ids)\
        .exclude(id=product.id)
    similar_products = similar_products.annotate(same_tags=Count('tags'))\
        .order_by('same_tags', '-created')[:2]
    share_string = quote_plus(product.name)
    return render(request,
                  'products/product_detail.html',
                  {'product': product,
                   'categories': categories,
                   'share_string': share_string,
                   'similar_products': similar_products})


def re_category(request):
    re_categories = ReCategory.objects.all()
    recipes = Recipe.objects.all()
    categories = Category.objects.all()

    return render(request, 'recipes/recipe_category.html', {
        're_categories': re_categories,
        'recipes': recipes,
        'categories': categories,
    })


def recipe_list(request, re_category_slug=None, tag_slug=None):
    recipes = Recipe.objects.all()
    categories = Category.objects.all()
    re_category = None
    re_categories = ReCategory.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        recipes = Recipe.objects.filter(tags__in=[tag])

    if re_category_slug:
        re_category = get_object_or_404(ReCategory, slug=re_category_slug)
        recipes = recipes.filter(re_category=re_category)

    return render(request,
                  'recipes/recipe_list.html',
                  {'re_category': re_category,
                   're_categories': re_categories,
                   'categories': categories,
                   'recipes': recipes,
                   'tag': tag,
                   })


def recipe_detail(request, id, slug, count=3):
    recipe = get_object_or_404(Recipe, id=id, slug=slug)
    categories = Category.objects.all().annotate(products_count=Count('products'))
    recipe_categories = ReCategory.objects.all()
    recipes = Recipe.objects.all()
    latest_recipes = Recipe.objects.order_by('created')[:count]
    recomments = recipe.recomments.filter(active=True)
    form = CommentForm()
    tags = Tag.objects.all()

    if recipe:
        recipe.views = recipe.views + 1
        recipe.save()

    return render(request, 'recipes/recipe_detail.html',
                  {'recipe': recipe,
                   'recipes': recipes,
                   'categories': categories,
                   'recipe_categories': recipe_categories,
                   'latest_recipes': latest_recipes,
                   'recomments': recomments,
                   'form': form,
                   'tags': tags})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'posts/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


@require_POST
def recipe_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comment = None
    form = RecipeCommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.recipe = recipe
        comment.save()
    return render(request, 'recipes/comment_recipe.html', {
        'recipe': recipe,
        'form': form,
        'comment': comment,
    })


def contact(request):
    if request.method == "POST":
        categories = Category.objects.all()
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        message = request.POST['message']

        send_mail(
            message_name,
            message_email,
            message,
            ['hasanmehedi570@gmail.com'],
        )
        return render(request, 'contact.html', {
            'message_name': message_name,
            'categories': categories,
        })

    else:
        categories = Category.objects.all()
        return render(request, 'contact.html', {'categories': categories, })


class SearchProducts(generic.View):
    def get(self, *args, **kwargs):
        key = self.request.GET.get('key', '')
        products = Product.objects.filter(
            Q(name__icontains=key) |
            Q(description__icontains=key)
        )
        posts = Post.published.filter(
            Q(title__icontains=key) |
            Q(body__icontains=key)
        )
        context = {
            'products': products,
            'posts': posts,
            'key': key,
        }
        return render(self.request, 'search_products.html', context)
