# -*- coding:utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError
from app01.models import User,Comment,Article
# from app01.models import GENDER_CHOICE,DEFAULT_GENDER
import re

class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                               max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                               max_length=20,error_messages={"required": "password不能为空",})
    v_code=forms.CharField(widget=forms.TextInput(attrs={'placeholder': '验证码','required':'required',}),
                           error_messages={'required':'验证码错误'})

# class RegForm(forms.Form):
#     '''
#     注册表单
#     '''
#     username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
#                                max_length=50,error_messages={"required": "username不能为空",})
#     email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
#                              max_length=50,error_messages={"required": "email不能为空",})
#     url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Url", }),
#                          max_length=100, required=False)
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
#                                max_length=20,error_messages={"required": "password不能为空",})

class RegForm(forms.ModelForm):
    re_password=forms.CharField(
        max_length=20,
        min_length=6,
        label='确认密码',
        widget=forms.widgets.PasswordInput(render_value=True)#回显数据
    )
    # gender=forms.ChoiceField(
    #     label='性别',
    #     widget=forms.widgets.RadioSelect(),
    #     choices=Hobby.objects.all().values_list('id','name'),
    #     # initial=DEFAULT_GENDER,
    # )


    # hobby=forms.ChoiceField(
    #     label='爱好',
    #     widget=forms.widgets.RadioSelect(),
    #     choices=Hobby.objects.all().values_list('id','name'),
    #     # initial=DEFAULT_GENDER,
    # )

    gender = forms.ChoiceField(
        label='性别',
        required=True,
        choices=(('male','男'),('female','女'),('unknown','保密')),
        initial=['unknown'],
        widget=forms.widgets.RadioSelect(),
        error_messages={
            'required': '性别不能为空'
        }
    )


    class Meta:
        model=User  #若views里用save注册，此处对应authUserInfo而非UsrInfo
        fields=['username','password','re_password','email','url','mobile']
        labels={
            'email':'邮箱',
            'password':'密码',
            'username':'用户名',
        }
        error_messages={
            'password':{
                'min-length':'密码最短6位'
            }
        }
        widgets={
            'password':forms.widgets.PasswordInput(),
            'email':forms.widgets.EmailInput()
        }

    # 定义全局的钩子，用来校验密码和确认密码字段是否相同
    def clean(self):
        password_value = self.cleaned_data.get('password')
        re_password_value = self.cleaned_data.get('re_password')
        if password_value == re_password_value:
            return self.cleaned_data
        else:
            self.add_error('re_password', '两次密码不一致')
            raise ValidationError('两次密码不一致')

        #局部钩子
    def clean_username(self):
        name_value=self.cleaned_data.get('username')
        print('value_name',name_value)
        print('%'*120)
        is_exit= User.objects.filter(username=name_value)
        if is_exit:
            raise ValidationError('用户名已存在')
        else:
            return name_value

    def clean_mobile(self):
        mobile=self.cleaned_data.get('mobile')
        print('value_mobile',mobile)
        print('%'*120)
        is_exit= User.objects.filter(mobile=mobile)
        if is_exit:
            raise ValidationError('手机号已存在')
        else:
            return mobile


    #https://www.cnblogs.com/liwenzhou/p/8747872.htmlauto
    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        # self.fields['hobby'].choices=Hobby.objects.all().values_list('id','name')
        for field in iter(self.fields):
            if field=='gender':
                break
            # if field=='hobby':
            #     break
                # self.fields[field].widget.attrs.update({'class'})
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class CommentForm(forms.Form):
    '''
    评论表单
    '''
    # author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
    #                                                        "required": "required","size": "25", "tabindex": "1"}),
    #                          max_length=50,error_messages={"required":"username不能为空",})
    # email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
    #                                                        "required":"required","size":"25", "tabindex":"2"}),
    #                          max_length=50, error_messages={"required":"email不能为空",})
    # url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
    #                                                    "size":"25", "tabindex":"3"}),
    #                      max_length=100, required=False)

    author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
                                                          "size": "25", "tabindex": "1"}),
                             max_length=50,required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
                                                           "size":"25", "tabindex":"2"}),
                             max_length=50,required=False)
    url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
                                                       "size":"25", "tabindex":"3"}),
                         max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "3", "tabindex": "4"}),
                              error_messages={"required":"评论不能为空",})
    article = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model=Comment  #若views里用save注册，此处对应authUserInfo而非UserInfo
        fields=['author','email','url','comment','article']
        labels={
            'email':'邮箱',
            'comment':'评论内容',
            'article':'文章',
        }

        widgets={
            'comment':forms.widgets.TextInput(),
            'email':forms.widgets.EmailInput()
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class PublishForm(forms.ModelForm):
    '''
    评论表单
    '''
    # author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
    #                                                        "required": "required","size": "25", "tabindex": "1"}),
    #                          max_length=50,error_messages={"required":"username不能为空",})
    # email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
    #                                                        "required":"required","size":"25", "tabindex":"2"}),
    #                          max_length=50, error_messages={"required":"email不能为空",})
    # url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
    #                                                    "size":"25", "tabindex":"3"}),
    #                      max_length=100, required=False)

    # author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
    #                                                        "size": "25", "tabindex": "1"}),
    #                          max_length=50,required=False)
    # email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
    #                                                        "size":"25", "tabindex":"2"}),
    #                          max_length=50,required=False)
    # url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
    #                                                    "size":"25", "tabindex":"3"}),
    #                      max_length=100, required=False)
    # comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
    #                                                        "required": "required", "cols": "25",
    #                                                        "rows": "3", "tabindex": "4"}),
    #                           error_messages={"required":"评论不能为空",})
    # article = forms.CharField(widget=forms.HiddenInput())
    #
    # class Meta:
    #     model=Comment  #若views里用save注册，此处对应authUserInfo而非UsrInfo
    #     fields=['author','email','url','comment','article']
    #     labels={
    #         'email':'邮箱',
    #         'comment':'评论内容',
    #         'article':'文章',
    #     }
    #
    #     widgets={
    #         'comment':forms.widgets.TextInput(),
    #         'email':forms.widgets.EmailInput()
    #     }
    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control'
    #         })
    click_count = forms.CharField(required=False, widget=forms.HiddenInput())
    class Meta:
        model=Article
        fields=['title','desc','category','tag']
        labels={
            'title':'输入文章标题',
            'desc':'输入文章描述',
            # 'user':'所属用户',
            'category':'输入文章分类',
            'tag':'选择文章标签',
        }
        # fields='__all__'