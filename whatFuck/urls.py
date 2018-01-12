# _*_ coding:utf-8 _*_

"""whatFuck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin
from whatFuck.settings import MEDIA_ROOT
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetUserPwdView, ModifyUserPwdView, \
    IndexView
from organization.views import OrgList

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active'),
    url(r'^forget_pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetUserPwdView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/', ModifyUserPwdView.as_view(), name='modify_pwd'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    # 配置静态文件文件的访问处理函数
    # url(r'^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),

    # 课程相关url 配置
    url(r'^course/', include('courses.urls', namespace='course')),
    # 个人信息url 配置
    url(r'^user/', include('users.urls', namespace='user')),
    # uediter url 配置
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

# 全局404
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.server_not_found'
