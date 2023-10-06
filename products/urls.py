from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:product_pk>/<str:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/comment/<int:product_pk>/', views.ProductCommentView.as_view(), name='product_comment'),
    path('product/like/<int:product_pk>/', views.ProductLikeView.as_view(), name='product_like'),
    path('product/dislike/<int:product_pk>/', views.ProductDislikeView.as_view(), name='product_dislike'),
    path('category/<int:category_pk>/', views.CategoryListView.as_view(), name='category_list'),
]
