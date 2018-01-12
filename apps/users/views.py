# _*_ coding:utf-8 _*_
import json

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UpdatePwdForm, UserInfoForm
from users.models import UserProfile, EmailVerifyRecord, Banner
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


# 自定义表单用户名
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.
class LoginView(View):
    def get(self, request):

        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': u'用户未激活！'})

            else:
                return render(request, 'login.html', {'msg': u'用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    '''
    用户登出
    '''

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': u'用户已存在！', 'register_form': register_form})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册暮雪网'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'index.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetUserPwdView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})


class ModifyUserPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')

            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不相等'})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserInfoView(View, LoginRequiredMixin):
    '''
    用户个人信息
    '''

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps('{"status":"success"}'), content_type='application/json')

        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(View, LoginRequiredMixin):
    '''
    用户修改头像
    '''

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps('{"status":"success"}'), content_type='application/json')
        else:
            return HttpResponse(json.dumps('{"status":"fail"}'), content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):
        modify_form = UpdatePwdForm(request.POST)
        if modify_form.is_valid():

            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({"status": "fail", 'message': '密码不一致'}),
                                    content_type='application/json')
            user = request.user
            user.password = pwd1
            user.save()
            return HttpResponse(json.dumps({"status": "success", 'message': '密码修改成功'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(View, LoginRequiredMixin):
    '''
    发送邮箱验证码
    '''

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps("{'email':'邮箱已经存在'}"), content_type='application/json')
        send_register_email(email, 'email_update')
        return HttpResponse(json.dumps('{"status":"success"}'), content_type='application/json')


class UpdateEmailView(View, LoginRequiredMixin):
    '''
    修改邮箱
    '''

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, type='email_update')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(json.dumps('{"status":"success"}'), content_type='application/json')

        else:
            return HttpResponse(json.dumps("{'email':'验证码出错'}"), content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        all_course = UserCourse.objects.filter(user=user)
        return render(request, 'usercenter-mycourse.html', {'all_course': all_course})


class MyFavOrgView(View, LoginRequiredMixin):
    def get(self, request):
        org_list = []
        all_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in all_fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'org_list': org_list})


class MyFavTeacherView(View, LoginRequiredMixin):
    def get(self, request):
        teacher_list = []
        all_fav_teacher = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in all_fav_teacher:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {'teacher_list': teacher_list})


class MyFavCourseView(View, LoginRequiredMixin):
    def get(self, request):
        course_list = []
        all_fav_course = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in all_fav_course:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'course_list': course_list})


class MyMessageView(View, LoginRequiredMixin):
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 第二个参数需要传递一个最小值，表示一页有多少个
        p = Paginator(all_message, 1, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'messages': messages})


class IndexView(View):
    def get(self, request):
        '''
        取出轮播图
        '''
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_org = CourseOrg.objects.all()[:15]
        return render(request, 'index.html',
                      {'all_banners': all_banners, 'courses': courses, 'banner_courses': banner_courses,
                       'course_org': course_org})


def page_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def server_not_found(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


# django 推荐使用类的方法，所以这个地方的 方法类型 不推荐
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': u'用户名或密码错误！'})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})

class LoginUnsafeView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')

        import MySQLdb
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='admin', db='mxonline', charset='utf8')
        cursor = conn.cursor()
        sql_select = "select * from users_userprofile where email='{0}' and password ='{1}'".format(user_name,
                                                                                                    pass_word)
        result = cursor.execute(sql_select)
        for row in cursor.fetchall():
            # 查询到用户
            pass
