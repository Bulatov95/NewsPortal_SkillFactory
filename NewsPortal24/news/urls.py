from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete, ProfileView, upgrade_me

urlpatterns = [
   path('', PostsList.as_view(), name = 'posts'),
   path('<int:pk>', PostDetail.as_view()),
   path('search/', PostSearch.as_view(), name='search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('profile/', ProfileView.as_view(), name='profile'),
   path('profile/upgrade/', upgrade_me, name='upgrade')
]