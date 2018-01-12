# _*_ coding:utf-8 _*_
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View

from operation.models import UserFavorite
from organization.models import CourseOrg, CityDict, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
import json


# Create your views here.

class OrgList(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        org_number = all_orgs.count()
        all_citys = CityDict.objects.all()

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 学习人数排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_num')

        # 取出排名前三的机构
        hot_orgs = all_orgs.order_by('-click_num')[:3]

        # 取出城市id
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        # 取出类别信息
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 第二个参数需要传递一个最小值，表示一页有多少个
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html',
                      {'all_orgs': orgs, 'all_citys': all_citys, 'org_numder': org_number, 'city_id': city_id,
                       'category': category, 'hot_orgs': hot_orgs, 'sort': sort})


class AddUserAskView(View):
    '''
    用户添加咨询
    '''

    def post(self, request):
        userask_from = UserAskForm(request.POST)
        if userask_from.is_valid():
            user_ask = userask_from.save(commit=True)
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加出错！'}), content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        corse_org = CourseOrg.objects.get(id=org_id)
        corse_org.click_num += 1
        corse_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=corse_org.id, fav_type=2):
                has_fav = True
        all_courses = corse_org.course_set.all()[:3]
        all_teacher = corse_org.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html',
                      {'all_courses': all_courses, 'all_teacher': all_teacher, 'corse_org': corse_org,
                       'current_page': current_page, 'has_fav': has_fav})


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        corse_org = CourseOrg.objects.get(id=org_id)
        all_courses = corse_org.course_set.all()[:3]
        return render(request, 'org-detail-course.html',
                      {'all_courses': all_courses, 'corse_org': corse_org, 'current_page': current_page})


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        corse_org = CourseOrg.objects.get(id=org_id)
        return render(request, 'org-detail-desc.html',
                      {'corse_org': corse_org, 'current_page': current_page})


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        corse_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = corse_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',
                      {'all_teacher': all_teacher, 'corse_org': corse_org, 'current_page': current_page})


class AddFavView(View):
    '''
    用户收藏
    '''

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户登陆状态
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_record:
            # 记录已经存在，表示用户取消收藏
            exist_record.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}), content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_type = int(fav_type)
                user_fav.fav_id = int(fav_id)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}), content_type='application/json')

            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错'}), content_type='application/json')


class TeacherListView(View):
    '''
    课程讲师列表页
    '''

    def get(self, request):
        all_teacher = Teacher.objects.all()

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teacher = all_teacher.order_by('-click_num')
        elif sort == '':
            all_teacher = Teacher.objects.all()

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teacher = all_teacher.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        sorted_teacher = Teacher.objects.all().order_by('-click_num')[:2]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 第二个参数需要传递一个最小值，表示一页有多少个
        p = Paginator(all_teacher, 1, request=request)

        teacher = p.page(page)

        return render(request, 'teachers-list.html',
                      {'all_teacher': teacher, "sorted_teacher": sorted_teacher, 'sort': sort})


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        sorted_teacher = Teacher.objects.all().order_by('-click_num')[:2]
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True
        return render(request, 'teacher-detail.html',
                      {'sorted_teacher': sorted_teacher, 'all_courses': all_courses, 'teacher': teacher,
                       'has_teacher_faved': has_teacher_faved, 'has_org_faved': has_org_faved})
