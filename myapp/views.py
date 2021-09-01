from django.shortcuts import render, resolve_url, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Post, Tag, Like, Contact, Opinion
from .forms import PostForm, LoginForm, SignUpForm, TagForm, SearchForm, ContactForm, OpinionForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import requests
import logging



class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.author == self.request.user


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
        post_list = Post.objects.all().order_by('-updated_at')
        context = {
            'post_list': post_list
        }
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:home')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'ブックマークを登録しました')
        return resolve_url('myapp:home')


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post


class PostUpdate(OnlyMyPostMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request, 'ブックマークを更新しました')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])


class PostDelete(OnlyMyPostMixin, DeleteView):
    model = Post
    
    def get_success_url(self):
        messages.info(self.request, 'ブックマークを削除しました')
        return resolve_url('myapp:home')


class PostList(ListView):
    model = Post
    paginate_by = 50

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


class TagList(ListView):
    model = Tag
    paginate_by = 30
    
    def get_queryset(self):
        return Tag.objects.all().order_by('-good')


class TagDetail(DetailView):
    model = Tag
    
    def get_context_data(self, *args, **kwargs):
        detail_data = Tag.objects.get(id = self.kwargs['pk'])
        tag_posts = Post.objects.filter(tag = detail_data.id).order_by('-created_at')

        params = {
            'object': detail_data,
            'tag_posts': tag_posts,
        }

        return params


class TagCreate(CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('myapp:home')

    def get_success_url(self):
        messages.success(self.request, 'タグを登録しました')
        return resolve_url('myapp:home')



@login_required
def Like_add(request, tag_id):
    tag = Tag.objects.get(id = tag_id)
    is_liked = Like.objects.filter(user = request.user, tag = tag_id).count()
    if is_liked > 0:
        messages.info(request, 'すでにお気に入りに追加済みです')
        return redirect('myapp:tag_detail', tag.id)

    like = Like()
    like.user = request.user
    like.tag = tag
    like.save()
    tag.good += 1
    tag.save()

    messages.success(request, 'お気に入りに追加しました！')
    return redirect('myapp:tag_detail', tag.id)



@login_required
def Like_delete(request, tag_id):
    tag = Tag.objects.get(id = tag_id)
    is_liked = Like.objects.filter(user = request.user, tag = tag_id).count()
    if is_liked <= 0:
        messages.info(request, 'お気に入りに入っていません')
        return redirect('myapp:tag_detail', tag.id)

    Like.objects.filter(user = request.user, tag = tag_id).delete()
    tag.good -= 1
    tag.save()

    messages.success(request, 'お気に入りを解除しました')
    return redirect('myapp:tag_detail', tag.id)


class LikeList(ListView):
    model = Like
    paginate_by = 5


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            search_list = Post.objects.filter(Q(title__icontains = freeword) |Q(memo__icontains = freeword))

        params = {
            'search_list': search_list,
        }

        return render(request, 'myapp/search.html', params)



class ContactCreate(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('myapp:index')

    def get_success_url(self):
        messages.success(self.request, 'お問い合わせを送信しました')
        return resolve_url('myapp:index')


class OpinionCreate(CreateView):
    model = Opinion
    form_class = OpinionForm
    success_url = reverse_lazy('myapp:home')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(OpinionCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'お問い合わせを送信しました')
        return resolve_url('myapp:home')