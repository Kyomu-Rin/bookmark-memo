from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import Post, Tag
from .forms import PostForm
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'myapp/index.html'


class HomeView(TemplateView):
    template_name = 'myapp/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list
        }
        return context


# 新規追加する
class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:home')
