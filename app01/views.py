# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render, redirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Count
from app01.models import *
from app01.forms import *
from django.http import JsonResponse
import random
from PIL import Image,ImageDraw,ImageFont

from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
logger = logging.getLogger('app01.views')

# Create your views here.
def middlewareLogin(request):
    if request.method=='POST':
        username=request.POST['username']
        v_code=request.POST['in_code'].upper()
        print(v_code,username)
        res={'code':0}
        if v_code==request.session.get('in_code'):
            username=request.POST['username']
            pwd=request.POST['pwd']
            mian=request.POST.get('mian')
            print(username,pwd)

            # user_obj=UserInfo.objects.filter(username=username,password=pwd).first()
            user_obj=auth.authenticate(username=username,password=pwd)#验证的是User表
            print(user_obj)
            if user_obj:
                auth.login(request,user_obj)
                # request.session['user_id']=user_obj.id
                if mian:#免登陆7天
                    request.session.set_expiry(7*24*60*60)
                else:
                    request.session.set_expiry(0)#退出浏览器清除
                #登陆成功
                res['next_url']='/index/'
                print(res)
                return JsonResponse(res)
                # return HttpResponse(json.dumps(res))
                # return redirect('/index/')
            else:
                res['code']=1
                res['err_msg']='用户名或密码错误'
                return JsonResponse(res)
            # return HttpResponse(json.dumps(res))
            # return HttpResponse('用户名或密码错误')
        else:
            res['code']=1
            res['err_msg']='验证码错误'
            return JsonResponse(res)

    return render(request, "middlewareLogin.html")
from django.views import View


# @method_decorator(csrf_exempt, name="get")
# @method_decorator(csrf_exempt, name="post")
import time
import os
import datetime as dt
import uuid
import json
@csrf_exempt
def upload(request):
    upload_file = request.FILES['editormd-image-file']
    if request.method == 'POST' and upload_file:
        success, message = 0, '上传失败'
        result = {"error": 1, "message": "上传出错"}


        allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
        file_suffix = upload_file.name.split(".")[-1]
        if file_suffix not in allow_suffix:
            return {"error": 1, "message": "图片格式不正确"}


        today = dt.datetime.today()
        dir_name = 'editormd' + '/%d/%d/' % (today.year, today.month)  #相对路径relative_path_file     kindeditor/2020/7/
        if not os.path.exists(settings.MEDIA_ROOT + dir_name):
            os.makedirs(settings.MEDIA_ROOT + dir_name)
        # return dir_name


        path = os.path.join(settings.MEDIA_ROOT, dir_name)
        if not os.path.exists(path):  # 如果目录不存在创建目录
            os.makedirs(path)
        file_name = str(uuid.uuid1()) + "." + file_suffix
        path_file = os.path.join(path, file_name)
        file_url = settings.MEDIA_URL + dir_name + file_name
        open(path_file, 'wb').write(upload_file.file.read())
        print(file_url)

        print('#'*120)
        result={"success": 1,
                'message': '上传成功',
                "url": file_url}

        return HttpResponse(json.dumps(result), content_type="application/json")


    #     # 本地创建保存图片的文件夹
    #     path = settings.MEDIA_ROOT + 'upload/' + time.strftime('%Y%m%d') + '/'
    #     # if not os.path.exists(settings.BASE_DIR + path):
    #     #     os.makedirs(settings.BASE_DIR + path)
    #
    #     today = dt.datetime.today()
    #     # dir_name = path + '/%d/%d/' % (today.year, today.month)
    #     if not os.path.exists( path):
    #         os.makedirs(path)
    #
    #     # 拼装本地保存图片的完整文件名
    #     filename = time.strftime('%H%M%S') + '_' + upload_file.name
    #     local_file = path + filename
    #
    #     # 写入文件
    #     with open(local_file, 'wb+') as f:
    #         for chunk in upload_file.chunks():
    #             f.write(chunk)
    #
    #         success, message = 1, '上传成功'
    #
    #     # 返回格式
    #     data = {
    #         'success': success,
    #         'message': message,
    #         'url': path + filename
    #     }
    #
    #     return JsonResponse(data)
    # else:
    #     return JsonResponse({'state': 0, 'message': 'Not support method or Can not get file'})


class AjaxUpLoad(View):
    def get(self,request):
        return render(request,'AjaxUpLoad.html')

    def post(self,request):
        file_obj=request.FILES.get('editormd-image-file')
        file_name=file_obj.name
        with open(file_name,'wb')as f:
            for i in file_obj.chunks():
                f.write(i)
        image_url="/uploads/kindeditor/2020/7/6c2af218-bc12-11ea-81ef-b025aa286f56.jpg"
        res = {
            'success': 1,
            'message': '图片上传成功',
            'url': image_url
        }
        return HttpResponse('上传成功')



def logout(request):
    # rep=redirect('/cookieLogin/')
    # rep.delete_cookie('h1')
    # return rep
    # request.session.delete()

    auth.logout(request)#auth退出登录，退出后允许匿名用户访问主页
    # request.session.flush()#中间件退出登陆
    return redirect('/middlewareLogin/')
def v_code(request):
    # with open(r'D:\PythonProjects\firstdjango\code.png','wb') as f:
    img_obj=Image.new('RGB',(150,25),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw_obj=ImageDraw.Draw(img_obj)
    font = ImageFont.truetype("C:\Windows\Fonts\Inkfree.ttf", 30, encoding="utf-8")
    tmp=[]
    for i in range(5):
        l=chr(random.randint(97,122))
        b=chr(random.randint(65,90))
        n=str(random.randint(0,9))

        t=random.choice([l,b,n])
        tmp.append(t)
        draw_obj.text((i*20+20,-5),t,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        # img_obj.save(f)

    request.session['in_code']=''.join(tmp).upper()

    from io import BytesIO
    f1=BytesIO()
    img_obj.save(f1,format='PNG')
    img_data=f1.getvalue()

    return HttpResponse(img_data,content_type='image/png')

def register(request):
    if request.method=='POST':
        # username=request.POST.get('username')
        # pwd=request.POST.get('password')

        res={'code':0}
        form_obj_recv= RegForm(request.POST)
        # print(form_obj_recv)
        # print('#'*120)
        if form_obj_recv.is_valid():
            # print(form_obj_recv)
            # print('#'*120)
            # form_obj_recv.cleaned_data.pop('re_password')
            # print(form_obj_recv.cleaned_data)
            # # UserInfo.objects.create(**form_obj_recv.cleaned_data)#自己写的注册
            # authUserInfo.objects.create_user(username=form_obj_recv.cleaned_data['username'],
            #                          password=form_obj_recv.cleaned_data['password'],
            #                          email=form_obj_recv.cleaned_data['email'],)
            #
            #方法二，form_obj是一个modelform对象，他和数据库里面的model类对应的
            user_obj=form_obj_recv.save()
            user_obj.set_password(user_obj.password)
            user_obj.save()#代码无提示，主要用于更新和编辑
            res['url']='/middlewareLogin/'
        else:
            res['code']=1
            res['error_msg']=form_obj_recv.errors
            print(form_obj_recv.errors)
            print(res)
        return JsonResponse(res)
    form_obj=RegForm()
    # return render(request,'reg.html',locals())#当前作用域的所有变量
    # return render(request,'reg.html',{'form_obj':form_obj,'request':request})
    return render(request,'register.html',{'form_obj':form_obj})

def global_setting(request):#在settings的templates中注册
    # 站点基本信息
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # 分类信息获取（导航数据）
    category_list = Category.objects.all()[:6]
    # 文章归档数据
    archive_list = Article.objects.distinct_date()
    # 广告数据
    # 标签云数据
    # 友情链接数据
    # 文章排行榜数据
    # 评论排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    return locals()

def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()
        article_list = getPage(request, article_list)

    except Exception as e:
        print (e)
        logger.error(e)
    return render(request, 'index.html', locals())

def archive(request):
    try:
        # 先获取客户端提交的信息
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())

# 按标签查询对应的文章列表
def tag(request):
    try:
        # 暂未实现
        pass
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())

# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        print(id)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} )
                                   # if request.user.is_authenticated() else{'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        print(comments)
        print(article)
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print (e)
        logger.error(e)
    return render(request, 'article.html', locals())

# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=request.user,
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user )
            # if request.user.is_authenticated() else None    username=comment_form.cleaned_data["author"]
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

def publish(request):
    if request.method=="POST":
        try:
            publish_form=PublishForm(request.POST)

            if publish_form.is_valid():
                #获取发布信息

                publish_content=Article.objects.create(
                    title=publish_form.cleaned_data['title'],
                    desc=publish_form.cleaned_data['desc'],
                    # content=publish_form.cleaned_data['content'],
                    content=request.POST.get('edit_content'),
                    # click_count=request.POST.get('click_count'),
                    # user=publish_form.cleaned_data['user'],
                    user=request.user,
                    category=publish_form.cleaned_data['category'],


                )
                publish_content.save()
                tag=request.POST.get('tag')
                print("tag:")
                print(tag)
                publish_content.tag.add(tag)
                return redirect('/index')

            else:
                return render(request, 'failure.html', {'reason': publish_form.errors})
        except Exception as e:
            logger.error(e)

    publish_form=PublishForm()
    return render(request,'publish.html',{'publish_form':publish_form})
# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print (e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())

