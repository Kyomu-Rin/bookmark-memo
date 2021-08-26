from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField('タグ', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    site_url = models.CharField('URL', max_length=200, blank=False, unique=True)
    memo = models.TextField('メモ', max_length=1000)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    tag = models.ManyToManyField(Tag, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    image = models.CharField(max_length=2000)
    title = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.site_url

