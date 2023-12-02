from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.OrderView.as_view(), name='order'),
    path('detail/<int:order_pk>/', views.OrderDetailsView.as_view(), name='order_detail'),
]
