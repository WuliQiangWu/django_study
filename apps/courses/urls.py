# _*_ coding:utf-8 _*_
# __author__ : 'aj'
# __date__ : '2017/12/22 下午2:41'
from django.conf.urls import url, include
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

]
