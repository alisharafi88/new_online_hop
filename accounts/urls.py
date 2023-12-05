from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('changepassword/', views.ChangePassword.as_view(), name='change_password'),
]
