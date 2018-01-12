# _*_ coding:utf-8 _*_
# __author__ : 'aj'
# __date__ : '2017/12/20 下午6:23'

from django import forms
from operation.models import AskUser
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = AskUser
        fields = ['name', 'mobile', 'cursor_name']

    def clean_mobile(self):
        '''
        验证手机号码是否合法
        '''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            return forms.ValidationError(u'手机号码非法', code='mobile_invalid')
