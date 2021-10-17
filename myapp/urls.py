from django.urls import path, include
from . import views

app_name = 'myapp'

urlpatterns = [
    path('',                         views.IndexView.as_view(),      name='index'),
    path('home',                     views.HomeView.as_view(),       name='home'),
    path('post_create',              views.PostCreate.as_view(),     name='post_create'),
    path('post_detail/<int:pk>',     views.PostDetail.as_view(),     name='post_detail'),
    path('post_update/<int:pk>',     views.PostUpdate.as_view(),     name='post_update'),
    path('post_delete/<int:pk>',     views.PostDelete.as_view(),     name='post_delete'),
    path('post_list',                views.PostList.as_view(),       name='post_list'),

    path('tag_list',                 views.TagList.as_view(),        name='tag_list'),
    path('tag_detail/<int:pk>',      views.TagDetail.as_view(),      name='tag_detail'),
    path('tag_create',               views.TagCreate.as_view(),      name='tag_create'),

    path('login',                    views.Login.as_view(),          name='login'),
    path('logout',                   views.Logout.as_view(),         name='logout'),
    path('signup',                   views.SignUp.as_view(),         name='signup'),

    path('like_add/<int:tag_id>',    views.Like_add,                 name='like_add'),
    path('like_delete/<int:tag_id>', views.Like_delete,              name='like_delete'),
    path('like_list',                views.LikeList.as_view(),       name='like_list'),

    path('search',                   views.Search,                   name='search'),
    path('contact',                  views.ContactCreate.as_view(),  name='contact'),
    path('opinion',                  views.OpinionCreate.as_view(),  name='opinion'),
]