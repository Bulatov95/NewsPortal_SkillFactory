from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .filters import PostFilter
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


