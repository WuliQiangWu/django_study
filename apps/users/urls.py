# _*_ coding:utf-8 _*_
# __author__ : 'aj'
# __date__ : '2017/12/29 下午1:54'

from django.conf.urls import url, include
from users.views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, MyCourseView, MyFavOrgView, \
    MyFavTeacherView, MyMessageView, LogoutView

urlpatterns = [
    # 用户信息页面
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    # 上传头像
    url(r'^image/upload', UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    url(r'^update/pwd', UpdatePwdView.as_view(), name='pwd_update'),
    # 发送邮箱验证码
    url(r'^sendEmail_code', SendEmailCodeView.as_view(), name='sendEmail_code'),
    # 修改邮箱
    url(r'^updateEmail', SendEmailCodeView.as_view(), name='updateEmail'),
    # 我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),
    # 我收藏的机构
    url(r'^my_fav/org/$', MyFavOrgView.as_view(), name='my_fav_org'),
    # 我收藏的讲师
    url(r'^my_fav/teacher/$', MyFavTeacherView.as_view(), name='my_fav_teacher'),
    # 我收藏的课程
    url(r'^my_fav/course/$', MyFavTeacherView.as_view(), name='my_fav_course'),
    # 我收藏的课程
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),
    # 用户登出
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
