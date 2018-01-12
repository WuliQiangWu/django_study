# _*_ coding:utf-8 _*_
import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from courses.models import Course, CourseResource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q

# Create your views here.
from operation.models import UserFavorite, CourseComponent, UserCourse


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_num')[:3]
        #  课程排序
        sort = request.GET.get('sort', '')

        # 课程搜索
        # name__icontains 会做类似于数据库like 的操作 i  表示忽略大小写
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))

        if sort:
            if sort == 'students':
                all_course = Course.objects.order_by('-students')
            elif sort == 'hot':
                all_course = Course.objects.order_by('-click_num')
        # 课程列表分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 第二个参数需要传递一个最小值，表示一页有多少个
        p = Paginator(all_course, 6, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {'all_course': courses, 'sort': sort, 'hot_courses': hot_courses})


class CourseDetailView(View):
    '''
    课程详情页
    '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程点击数加1
        course.click_num += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course.id):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html',
                      {'course': course, 'relate_courses': relate_courses, 'has_fav_course': has_fav_course,
                       'has_fav_org': has_fav_org})


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        all_reousrce = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html',
                      {'course': course, 'all_reousrce': all_reousrce, 'relate_courses': relate_courses})


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        all_reousrce = CourseResource.objects.filter(course=course)
        all_comment = CourseComponent.objects.all()
        return render(request, 'course-comment.html',
                      {'course': course, 'all_reousrce': all_reousrce, 'all_comment': all_comment,
                       'relate_courses': relate_courses})


class AddCommentView(View):
    '''
    用户添加课程评论
    '''

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComponent()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')
