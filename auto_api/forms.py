# -*- coding:utf-8 -*-
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        '''告诉Django哪个模型会被用来创建这个表单（model=Post）'''
        model = Post
        fields = ('title', 'body')
