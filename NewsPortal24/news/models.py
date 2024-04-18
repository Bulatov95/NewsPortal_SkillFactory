from django.contrib.auth.models import User
from django.db import models



class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete= models.CASCADE)
    author_rating = models.IntegerField(default=0)

class Category(models.Model):
    name = models.CharField(max_length= 255, unique= True)


class Post(models.Model):
    news = 'NW'
    article = 'AR'
    CATEGORY = (
        (news, 'Новость'),
        (article, 'Статья'),
    )
    post_author = models.ForeignKey(Author, on_delete= models.CASCADE)
    nw_ar = models.CharField(max_length=2, choices=CATEGORY, default=news)
    time_in = models.DateTimeField(auto_now_add= True)
    category = models.ManyToManyField(Category, through= 'PostCategory')
    tittle = models.CharField(max_length= 255)
    text_post = models.TextField()
    post_rating = models.IntegerField(default= 0)

    def update_rating(self):
        pass
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
    post_comment = models.ForeignKey(Post, on_delete= models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete= models.CASCADE)
    text_comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add= True)
    comment_rating = models.IntegerField(default= 0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


