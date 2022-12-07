from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) :
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog') 

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='posts')
    body = RichTextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255, default='')
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog') 

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()

class History(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='histories')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.post.title, self.author.username)