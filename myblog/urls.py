"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from app01.views import *
from django.views import static
from django.conf import settings
from app01.uploads import upload_image
urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^index/$', index, name='index'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^article/$', article, name='article'),
    url(r'^publish/$', publish, name='publish'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
    url(r'^logout/$', do_logout, name='logout'),
    # url(r'^reg/$', do_reg, name='reg'),
    url(r'^reg/$', register, name='reg'),
    # url(r'^login', do_login, name='login'),


    url(r'^middlewareLogin/$', middlewareLogin, name='login'),
    url(r'^v_code/$',v_code,name='v_code'),
    url(r'^logout/$',logout),

    # url(r'^AjaxUpLoad/$',AjaxUpLoad.as_view()),
    url('^upload/$',upload,name='upload'),
    url(r'^category/$', category, name='category'),

    url(r"^uploads/(?P<path>.*)$", static.serve, {"document_root": settings.MEDIA_ROOT},),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r'^$', index, name='index'),


]
