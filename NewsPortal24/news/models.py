from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete= models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        # Изначально мы получаем QuerySet со всеми постами автора, агрегируем их, суммируя райтинг постов и получаем словарь
        # {'par3' : ЗНАЧЕНИЕ суммы рейтингов} и обращаемся к нему по ключу (Если бы мы не задали название ключа в aggregate,
        # то оно бы было стандартное для поля с рейтингоv в классе Post). Функция Coalesce нужна для замены None на 0, если
        # у нас отсутствуют статьи автора комментарии к ним и его комментарии, чтобы не получать ошибку при сложении в конечном выражении.
        post_author_rating3 = Post.objects.filter(post_author = self).aggregate(par3 =Coalesce(Sum('post_rating'), 0))['par3']
        comment_author_rating = Comment.objects.filter(user_comment =self.author_user).aggregate(car =Coalesce(Sum('comment_rating'), 0))['car']
        post_comment_rating = Comment.objects.filter(post__post_author = self).aggregate(pcr = Coalesce(Sum('comment_rating'), 0))['pcr']

        self.author_rating = 3 * post_author_rating3 + comment_author_rating + post_comment_rating
        self.save()

    def __str__(self):
        return f'{self.author_user}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    news = 'NW'
    article = 'AR'
    CATEGORY = (
        (news, 'Новость'),
        (article, 'Статья'),
    )
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    nw_ar = models.CharField(max_length=2, choices=CATEGORY, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    tittle = models.CharField(max_length=255)
    text_post = models.TextField()
    post_rating = models.IntegerField(default=0)

    # def __str__(self):
    #     return f'{self.tittle[:20]}: {self.post_author}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[0:123]}...'


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions',)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions',)