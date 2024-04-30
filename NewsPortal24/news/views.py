from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'Posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = super().get_queryset().filter(nw_ar = 'NW').count()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'


