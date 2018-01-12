# _*_ coding:utf-8 _*_
# __author__ : 'aj'
# __date__ : '2017/12/12 下午5:41'

from .models import CityDict, CourseOrg, Teacher

import xadmin


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'add_time', 'fav_num', 'image', 'address', 'city']
    search_fields = ['name', 'desc', 'fav_num', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'add_time', 'fav_num', 'image', 'address', 'city']
    relfield_style = 'fx-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'fav_num',
                    'add_time']
    search_fields = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'fav_num']
    list_filter = ['org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'fav_num',
                   'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
