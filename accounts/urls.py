from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('changepassword/', views.ChangePassword.as_view(), name='change_password'),
    path('changeAddress/<int:address_pk>/', views.ChangeAddress.as_view(), name='change_address'),
    path('removeAddress/<int:address_pk>/', views.RemoveAddress.as_view(), name='remove_address'),
    path('addAddress/', views.AddAddress.as_view(), name='add_address'),
]
