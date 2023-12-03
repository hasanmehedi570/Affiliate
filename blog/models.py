
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    featured = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='images/post_images/', null=True, blank=True)
    image2 = models.ImageField(
        upload_to='images/post_images/', null=True, blank=True)
    image3 = models.ImageField(
        upload_to='images/post_images/', null=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post_1 = models.BooleanField(default=False)
    post_2 = models.BooleanField(default=False)
    post_3 = models.BooleanField(default=False)
    post_4 = models.BooleanField(default=False)
    post_5 = models.BooleanField(default=False)

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    tags = TaggableManager()

    class Meta:
        ordering = ['publish']
        indexes = [
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:single_post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    image = models.ImageField(
        upload_to='images/categories/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to='images/product_images/%Y/%m/%d', blank=True)
    image_2 = models.ImageField(
        upload_to='images/product_images/%Y/%m/%d', null=True, blank=True)
    image_3 = models.ImageField(
        upload_to='images/product_images/%Y/%m/%d', null=True, blank=True)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5,
                                decimal_places=2)
    old_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:product_detail',
                       args=[self.id, self.slug])


class ReCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=300)
    image = models.ImageField(
        upload_to='images/Re_categories/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 're_category'
        verbose_name_plural = 're_categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:recipe_list_by_category',
                       args=[self.slug])


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.DurationField(default=timedelta(minutes=30))
    featured = models.BooleanField(default=True)
    description = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()
    step1 = models.TextField()
    step2 = models.TextField()
    step3 = models.TextField()
    step4 = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    serve = models.IntegerField(default=4)

    image = models.ImageField(
        upload_to='images/recipe_images/', blank=True, null=True)
    re_category = models.ForeignKey(
        ReCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def update_views(self, *args, **kwargs):
        self.views = self.views + 1
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:recipe_detail',
                       args=[self.id, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class RecipeComment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recomments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.recipe}'
