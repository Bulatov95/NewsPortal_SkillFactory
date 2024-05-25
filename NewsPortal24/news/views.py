from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

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

class PostCreate(PermissionRequiredMixin, CreateView,):
    permission_required = ('news.add_post',)
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

class PostEdit(PermissionRequiredMixin, UpdateView,):
    raise_exception = True
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'Post_create.html'
    success_url = reverse_lazy('posts')



class PostDelete(PermissionRequiredMixin, DeleteView,):
    raise_exception = True
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'Post_delete.html'
    success_url = reverse_lazy('posts')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'Profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='author').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        authors_group.user_set.add(user)
    return redirect('/News/profile/')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(Subscriber.objects.filter(user=request.user, category=OuterRef('pk')))).order_by('name')
    return render(request, 'Subscriptions.html', {'categories': categories_with_subscriptions})