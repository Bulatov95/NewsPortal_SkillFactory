from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import PostFilter
from .forms import PostForm
from .models import *

class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'Posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    # Метод для вывода количества новостей на страницу
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['news_count'] = super().get_queryset().filter(nw_ar = 'NW').count()
    #     return context

    # Метод для вывода количества постов на страницу
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_count'] = super().get_queryset().all().count()
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'Search.html'
    context_object_name = 'postssearch'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'Post_create.html'
    success_url = reverse_lazy('posts')

    # Здесь предопределяем для формы, по ссылке /articles/create/, что мы создаём статью.
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.nv_ar = 'AR'
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_title'] = self.get_type()['title']
        context['get_header'] = self.get_type()['header']
        return context

    def get_type(self):
        if self.request.path == '/articles/create/':
            return {'title': 'Create article', 'header': 'Добавить статью'}
        else:
            return {'title': 'Create News', 'header': 'Добавить новость'}

class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'Post_create.html'
    success_url = reverse_lazy('posts')


class PostDelete(DeleteView):
    model = Post
    template_name = 'Post_delete.html'
    success_url = reverse_lazy('posts')



