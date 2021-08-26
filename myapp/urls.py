from django.urls import path, include
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home', views.HomeView.as_view(), name='home'),
    path('post_create', views.PostCreate.as_view(), name='post_create'),
]