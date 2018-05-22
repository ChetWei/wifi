from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response,reverse
from django.contrib.auth import authenticate,login,logout  #登录,退出
from django.contrib.auth.backends import ModelBackend #邮箱登录验证
from django.db.models import Q #并且判断
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password #密码加密存储


import json
from .models import UserProfile,EmailVerifyRecord,Banner,LoginBanner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm ,UploadImageForm,UserInfoForm #表单数据库合法的验证
from utils.email_send import send_email #发送邮箱验证
from utils.mixin_utils import LoginRequiredMixin #登录验证
from pure_pagination import PageNotAnInteger,EmptyPage,Paginator #分页模块
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from course.models import Course


# Create your views here.


'''首页'''
class IndexView(View):
    def get(self,request):
        #取出所有课程轮播图
        all_banners = Banner.objects.all().order_by('index')
        course_images = Course.objects.filter(is_banner=False)[:5] #取出五个非轮播图obj
        course_banners = Course.objects.filter(is_banner=True)[:3]#取出三个轮播图obj
        #取出所有机构图
        org_images = CourseOrg.objects.all()[:15]

        return render(request,'index.html',{
            'all_banners' : all_banners,
            'course_images' : course_images,
            'course_banners' : course_banners,
            'org_images' : org_images,

        })


'''用户登录'''
class LoginView(View): #使用cbv模式，自动判别提交方法并分配


    def get(self,request):
        login_banners = LoginBanner.objects.all().order_by('index')
        return render(request, 'login.html',{
            'login_banners':login_banners,
        })


    def post(self,request):
        #实例化forms表单验证
        login_form = LoginForm(request.POST)

        if login_form.is_valid(): #判断用户名或密码是否存在,与数据库验证

            # 获取用户提交的用户名和密码
            user_name = request.POST.get("username",None)
            pass_word = request.POST.get("password",None)
            # 用自带的方法判断提交的用户名和密码是否合法，合法返回对象，不合法None
            user = authenticate(username=user_name,password=pass_word)

            if user is not None:  #输入合法
                #使用 login() 。该函数接受一个 HttpRequest 对象和一个 User 对象作为参数并使用Django的会话（ session ）框架把用户的ID保存在该会话中。
                user_status = UserProfile.objects.get(username = user_name)
                if user_status.is_active  :   #判断用户是否激活
                    login(request,user)
                    return HttpResponseRedirect(reverse("index")) #重定向到index地址

                else: #用户没有激活
                    return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})

            # 此时用户密码都存在，应该判断正确与否
            else:
                return render(request,'login.html',{'erroMsg':'用户名或密码错误'})

        else:   # form.is_valid()已经判断不合法了，用户名或密码不存在，返回login_form错误信息到前端，
            return render(request,'login.html',{'login_form':login_form})


'''用户退出'''
class LogoutView(View):
    def get(self,request):
        logout(request)
        #重定向
        from  django.urls import reverse
        return HttpResponseRedirect(reverse('index'))


'''全局404,500'''
def page_not_found(request):
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response



'''用户注册'''
class ResgisterView(View):


    def get(self,request):
        register_form = RegisterForm()
        login_banners = LoginBanner.objects.all().order_by('index')
        return render(request,"register.html",{
            'register_form':register_form,
            'login_banners':login_banners,
        })

    def post(self,request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid(): #如果邮箱,密码不为空
            user_email = request.POST.get("email",None)
            if UserProfile.objects.filter(email = user_email): #如果邮箱存在
                return render(request,'register.html',{'register_form':register_form,'msg':'邮箱已被注册'})

            user_pwd = request.POST.get("password",None)

            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_email   #用户邮箱当做用户名实现邮箱登入
            user_profile.email = user_email
            user_profile.is_active = False #默认添加的用户是激活状态,修改只有用户去邮箱激活之后才改为True
            user_profile.password = make_password(user_pwd) # 对保存到数据库的密码加密

            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile
            user_message.message = '欢迎注册慕学网！'
            user_message.save()

            send_email(user_email,'register') #发送验证码

            return render(request,'login.html')

        else:
            return render(request,'register.html',{'register_form':register_form})



'''用户邮箱激活'''
class ActiveUserView(View):
    def get(self,request,active_code):
        #查询邮箱验证记录是否存在
        email_lists = EmailVerifyRecord.objects.filter(code = active_code)

        if email_lists:#如果存在
            for email_list in email_lists:
                #获取到对应的邮箱
                email = email_list.email
                #查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True    #激活邮箱状态
                user.save()
                # 激活成功跳转到登录页面
                return render(request, 'login.html')

        else: #验证码在数据库中不存在的时候跳转到激活页面
            return render(request,'active_fail.html')


'''忘记密码'''
class ForgetpwdView(View):

    def get(self,request):
        forget_form = ForgetForm()
        login_banners = LoginBanner.objects.all().order_by('index')
        return render(request,"forgetpwd.html",locals())

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        # 校验合法
        if forget_form.is_valid():
            foget_email = request.POST.get("email",None)
            # 判断邮箱是否存在
            if EmailVerifyRecord.objects.filter(email=foget_email):

                send_email(foget_email,'forget')  #发送找回密码的链接

                return render(request,'send_success.html')
            else:#邮箱不存在
                return render(request,'forgetpwd.html',{'msg':'邮箱账号不存在'})

        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


'''重置密码邮箱链接跳转激活 get方式'''
class ResetView(View):
    def get(self,request,reset_code):
        #筛选数据库中的code等于用户code 的记录
        code_lists = EmailVerifyRecord.objects.filter(code=reset_code)
        if code_lists: #如果存在
            for code_list in code_lists:
                forgeted_email = code_list.email #取出用户邮箱号,传给给重置页面
                return render(request,'reset_pwd.html',{'forgeted_email':forgeted_email})
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


'''未登录重置密码post方式'''
class ModifyPwdView(View):
    def post(self,request):

        modify_form = ModifyPwdForm(request.POST)

        if modify_form.is_valid():

            pwd1 = request.POST.get("password1",None)
            pwd2 = request.POST.get('password2',None)
            forgeted_email = request.POST.get('email')

            if pwd1 != pwd2:
                return render(request,'reset_pwd.html',{'forgeted_email':forgeted_email},{'msg':'密码不一致'})

            else:
                UserProfile.objects.filter(email=forgeted_email).update(password = make_password(pwd1))
                return render(request,'login.html')
        else:

            forgeted_email = request.POST.get('forgeted_email',None)
            return render(request,'reset_pwd.html',{'forgeted_email':forgeted_email},{'modify_form':modify_form})



'''用户个人信息'''
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html')

    #post提交保存个人信息的修改
    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance = request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return  HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse(json.dumps((user_info_form)),content_type='application/json')




'''用户头像修改'''
class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user) #实例化图片上传form,带有form和model
        if image_form.is_valid():   #如果上传合法
            image_form.save()     #直接保存到数据库
            HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            HttpResponse("{'status':'fail'}",content_type='application/json')



'''已登录用户密码修改'''
class PwdUpdateView(LoginRequiredMixin,View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)

        if modify_form.is_valid(): #判断填写字符是否合法
            print('hello!')
            pwd1 = request.POST.get("password1",None)
            pwd2 = request.POST.get('password2',None)
            if pwd1 != pwd2:
                HttpResponse("{'status':'fail','msg':'密码不一致'}",content_type='application/json')

            else:
                user = request.user
                user.password = make_password(pwd1)
                user.save()
                HttpResponse("{'status':'success'}",content_type='application/json')

        else:
            HttpResponse(json.dumps(modify_form.errors), content_type='application/json')



'''发送修改邮箱验证'''
class SendEmailCodeView(View):
    def get(self,request):

        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email':'邮箱已存在'}",content_type='application/json')
        send_email(email,'update_email')
        return HttpResponse("{'status':'success'}", content_type='application/json')


'''修改邮箱'''
class UpdateEmail(View):
    def post(self,request):
        #获取post提交来的表单信息
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        #判断要更新的邮箱和验证码，以及验证类型是否存在
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
        else:
            HttpResponse("{'status':'fail','email':'验证码无效'}", content_type='application/json')



'''我的课程'''
class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        #获取用户课程的对象
        user_courses = UserCourse.objects.filter(user=request.user)

        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses,
        })


'''我的消息'''
class MyMsgView(LoginRequiredMixin,View):
    def get(self,request):
        #获取所有的消息
        all_message = UserMessage.objects.filter(user=request.user.id )
        unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)#获取所有已读消息
        #当进入页面时将所有的未读消息设为已读
        for unread_message in unread_messages:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4, request=request)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
        })



'''我的收藏，机构'''
class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2) #找到所有userfavorite对象
        #遍历userfavorite对象，取出所有的fav_id,再通过fav_id找到课程机构CourseOrg 的对象,将对象放在列表里
        org_list = []
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id #fav_id的id与被收藏对象的id是一样的
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list,
        })


'''我的收藏，课程'''
class MyFavCourseView(LoginRequiredMixin,View):
    def get(self,request):
        fav_courses = UserFavorite.objects.filter(user = request.user,fav_type=1)
        course_list = []
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id = course_id)
            course_list.append(course)

        return render(request,'usercenter-fav-course.html',{
            'course_list':course_list,
        })


'''我的收藏，讲师'''
class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self, request):

        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_list = []
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })








'''
让用户可以通过邮箱或者用户名都可以登录，用自定义authenticate方法
这里是继承ModelBackend类来做的验证
邮箱和用户名都可以登录
基础ModelBackend类，因为它有authenticate方法
'''

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))#二选一

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None



