from django.db import models


class Post(models.Model):
    """
    掲示板への投稿内容
    """
    content = models.CharField(max_length=140, help_text='掲示板の投稿内容')