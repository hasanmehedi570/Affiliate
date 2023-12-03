from django.urls import path
from . import views
from .views import SearchProducts


app_name = 'blog'

urlpatterns = [
    path('blogview/tag/<slug:tag_slug>/',
         views.blog_view, name='blog_view_by_tag'),

    path('', views.home, name='post_list'),
    path('tag/<slug:tag_slug>/', views.home, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.single_post_detail, name='single_post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),



    path('product/', views.product_list, name='product_list'),
    path('product/<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('blogview/', views.blog_view, name='blog_view'),
    path('product/tag/<slug:tag_slug>/',
         views.product_list, name='product_list_by_tag'),


    path('recipes/<int:recipe_id>/comment/',
         views.recipe_comment, name='recipe_comment'),
    path('re_category/', views.re_category, name='re_category'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<slug:re_category_slug>/', views.recipe_list,
         name='recipe_list_by_category'),
    path('recipes/<int:id>/<slug:slug>/',
         views.recipe_detail, name='recipe_detail'),
    path('recipes/tag/<slug:tag_slug>/',
         views.recipe_list, name='recipes_by_tag'),
    path('recipes/<int:id>/', views.recipe_detail,
         name='recipe_detail_by_views'),


    path('contact/', views.contact, name='contact'),
    path('search_products/', SearchProducts.as_view(), name='search_products'),
]
