# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'auto_api/post_detail.html', {'post': post})


def index(request):
    List = map(str, range(100))  # 一个长度为100的 List
    return render(request, 'auto_api/home.html', {'List': List})


def post_list(request):
    posts = Post.objects.filter(publish__lte=timezone.now()).order_by('publish')
    return render(request, 'auto_api/post_list.html', {'posts': posts})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish = timezone.now()
            post.save()
            # 保存后跳转到详情页面
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'auto_api/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'auto_api/post_edit.html', {'form': form})
