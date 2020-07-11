from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect ,HttpResponse

# class M1(MiddlewareMixin):
#     def process_request(self, request):
#         print(request)
#         print('in M1')
#     def process_response(self, request, response):
#         print(request)
#         print('in M1 process_response')
#         return response
#
# class M2(MiddlewareMixin):
#     def process_request(self,request):
#         print(request)
#         print('in M2 ')
#     def process_response(self, request, response):
#         print(request)
#         print('in M2 process_response')
#         return response
#     #返回响应时倒序
from django.conf import settings
# from app01.models import User,UserInfo
import time
# class CheckLogin(MiddlewareMixin):
#     def process_request(self,request):
#         #判断配置项是否有配置，没有则初始化一个列表
#         # while_urls=settings.WHITE_URLS if settings.WHITE_URLS else []
#         while_urls=settings.WHITE_URLS if hasattr(settings,'WHITE_URLS') else []
#         #判断是否在白名单,在就放行
#         if request.path_info in while_urls:
#             return None
#         #从session中获取user_id，如果有，则登陆过，无则跳转到登陆页面
#         user_id=request.session.get('user_id',None)
#         print(user_id)
#         print('$'*120)
#         if not user_id:
#             return redirect('/middlewareLogin/')
#         else:
#             user_obj=UserInfo.objects.get(id=user_id)
#             print(user_obj.username)
#             #把user对象赋值给request对象自定义属性user
#             request.user=user_obj.username

ACCESS_RECORD={}
class Throttle(MiddlewareMixin):
    def process_request(self,request):

        access_limit=settings.ACCESS_LIMIT if hasattr(settings,'ACCESS_LIMIT') else 1
        ip=request.META.get('REMOTE_ADDR')
        if ip not in ACCESS_RECORD:
            ACCESS_RECORD[ip]=[]
        history=ACCESS_RECORD[ip]
        now=time.time()

        while history and now-history[-1]>access_limit:
            history.pop()#长度超过三，把旧的记录pop掉
        history.insert(0,now)#把最新的插入最前面
        if len(history)>3:
            return HttpResponse('访问过于频繁，请稍后!')