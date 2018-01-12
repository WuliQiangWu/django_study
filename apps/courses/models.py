# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.Content = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath='course/uediter/',
                                           filePath='course/uediter/', default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=2)
    learn_time = models.IntegerField(default=0, verbose_name=u'分钟数')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(max_length=100, verbose_name=u'课程类别', default=u'后端开发')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    tag = models.CharField(default='', verbose_name=u'课程标签', max_length=50)
    need_know = models.CharField(max_length=300, verbose_name=u'课程须知', null=True, blank=True, default='')
    teacher_know = models.CharField(max_length=300, verbose_name=u'老师告诉你', null=True, blank=True, default='')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取章节数
        return self.lesson_set.all().count()

    get_zj_nums.short_description = u'章节数'

    def go_to(self):
        # from django.utils.safestring import mark_safe
        from django.utils.safestring import mark_safe
        return mark_safe('<a href = "https://www.baidu.com">自行查看</a>')

    go_to.short_description = u'跳转'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_lesson(self):
        # 获取课程章节
        return self.lesson_set.all()

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播图课程'
        verbose_name_plural = u'轮播图课程'
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_videos(self):
        # 获取章节视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'视频')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    url = models.CharField(max_length=200, default='', verbose_name=u'章节地址')
    long_time = models.IntegerField(default=0, verbose_name=u'视频时长')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'资源')
    download = models.FileField(upload_to='courses/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    name = models.CharField(max_length=100, verbose_name=u'名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'资源'
        verbose_name_plural = verbose_name
