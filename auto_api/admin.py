# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# Register your models here.
from django.contrib import admin
from .models import Article, Person, Post


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'update_time', )
    def save_model(self, request, obj, form, change):
        '''
        修改保存时的一些操作，可以检查用户，保存的内容等，比如保存时加上添加人
        其中obj是修改后的对象，form是返回的表单（修改后的），
        当新建一个对象时 change = False, 当修改一个对象时 change = True
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        '''
        if change:# 更改的时候
            obj_original = self.model.objects.get(pk=obj.pk)
        else:# 新增的时候
            obj_original = None
        obj.user = request.user
        obj.save()

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        # handle something here
        obj.delete()


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', )
    search_fields = ('name', )

    def get_search_results(self, request, queryset, search_term):
        '''
        定制搜索功能
        queryset 是默认的结果，search_term 是在后台搜索的关键词
        :param request:
        :param queryset:
        :param search_term:
        :return:
        '''
        queryset, use_distinct = super(PersonAdmin,self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct




class MyModleAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        '''
        该类实现的功能是如果是超级管理员就列出所有的，
        如果不是，就仅列出访问者自己相关的
        :param request:
        :return:
        '''
        qs = super(MyModleAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish','status')

admin.site.register(Article)
admin.site.register(Person)
admin.site.register(Post,PostAdmin)

