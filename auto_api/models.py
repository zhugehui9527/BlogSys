# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def my_property(self):
        return self.first_name + ' ' + self.last_name

    my_property.short_description = "Full name of the person"

    full_name = property(my_property)


# 兼容python2.x和python3.x
# @python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField('标题', max_length=256)
    content = models.TextField('内容')
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __unicode__(self):
        # 在Python3中用 __str__ 代替 __unicode__
        return self.title


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Published')
    )
    # title： 这个字段对应帖子的标题
    title = models.CharField(max_length=250)
    # slug就是一个短标签
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # author：这是一个ForeignKey。这个字段定义了一个多对一（many-to-one）的关系
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish', )

    def __unicode__(self):
        return self.title


