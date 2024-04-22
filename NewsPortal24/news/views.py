from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

class PostsList(ListView):
    model = Post
    ordering = '-post_rating'
    template_name = 'Posts.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'


