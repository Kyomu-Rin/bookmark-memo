from django.shortcuts import render, resolve_url
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Post, Tag
from .forms import PostForm, LoginForm, SignUpForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
import requests
import logging


class IndexView(TemplateView):
    template_name = 'myapp/index.html'
    print('IndexView')
    logging.debug('debug message')


class HomeView(TemplateView):
    template_name = 'myapp/home.html'
    print('homeView')
    logging.debug('debug message')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list
        }
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:home')


class PostDetail(DetailView):
    model = Post


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request, 'Postを更新しました')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])


class PostDelete(DeleteView):
    model = Post
    
    
    def get_success_url(self):
        messages.info(self.request, 'Postを削除しました')
        return resolve_url('myapp:home')


class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'


class Logout(LogoutView):
    template_name = 'myapp/logout.html'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'ユーザー登録をしました')
        return HttpResponseRedirect(self.get_success_url())
