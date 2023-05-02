from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from comment.models import Comment


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.item

class FavoriteList(models.Model):
    username = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)

class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    comments = GenericRelation(Comment)
    favoriteLists = models.ManyToManyField(FavoriteList, related_name='favoriteBooks')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})


class Rating(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'user')
