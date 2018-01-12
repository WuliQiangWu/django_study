# _*_ coding:utf-8 _*_
# __author__ : 'aj'
# __date__ : '2017/12/12 下午5:59'

from .models import AskUser, CourseComponent, UserFavorite, UserMessage, UserCourse

import xadmin


class AskUserAdmin(object):
    list_display = ['name', 'mobile', 'cursor_name', 'add_time']
    filter_fields = ['name', 'mobile', 'cursor_name']
    list_filter = ['name', 'mobile', 'cursor_name', 'add_time']


class CourseComponentAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    filter_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    filter_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    filter_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    filter_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']


xadmin.site.register(AskUser, AskUserAdmin)
xadmin.site.register(CourseComponent, CourseComponentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
