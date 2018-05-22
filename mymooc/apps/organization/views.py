# _*_ encoding:utf-8 _*_

from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate,login  #登录
from django.db.models import Q


from pure_pagination import PageNotAnInteger,EmptyPage,Paginator #分页模块
from .models import CityDict,CourseOrg,Teacher
from course.models import Course
from operation.models import UserFavorite
from .forms import UserAskForm
import json


'''课程机构'''
class OrgView(View):

    def get(self,request):
        city_lists = CityDict.objects.all()  #选出所有的城市
        org_lists = CourseOrg.objects.all() #选出所有的机构

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            org_lists = CourseOrg.objects.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(address__icontains=search_keywords))


        hot_orgs = org_lists.order_by('fav_nums')[:3] #热门机构按照收藏人数排名，取前三

        #取出筛选机构类型
        org_catgory = request.GET.get('catgory','')
        if org_catgory:
            org_lists = org_lists.filter(catgory = org_catgory)

        #取出筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            org_lists = org_lists.filter(city_id = int(city_id))

        orderBy = request.GET.get('sort')  # 获取排序规则
        if orderBy:
            if orderBy == 'students':  # 按学习人数排序
                org_lists = org_lists.order_by('-students')
            elif orderBy == 'courses':  # 按课程数排序
                org_lists = org_lists.order_by('-course_nums')



        org_num = org_lists.count()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        # 这里指从 org_lists 中取五个出来，每页显示3个
        p = Paginator(org_lists, 3, request=request)

        orgs = p.page(page)  #

        return render(request, 'org-list.html', {
            'city_lists':city_lists,
            'org_lists':orgs,  #
            'org_num':org_num,

            'org_catgory': org_catgory,  # 筛选的机构
            'city_id':city_id,  #提交的城市id

            'hot_orgs':hot_orgs,#热门机构

            'orderBy':orderBy, #排序规则
        })


'''用户咨询'''
class UserAskView(View):

    def post(self,request):

        userask_form =UserAskForm(request.POST) #自定义验证方式

        msg = {'status': 'success'}
        if userask_form.is_valid(): #判断合法
            user_ask = userask_form.save(commit=True) #如果验证合法，直接保存到数据库

            msg = json.dumps(msg)
            return HttpResponse(msg,content_type='application/json')
        else:
            msg['status'] = 'faild'
            msg['msg'] = '提交失败,请重试'

            msg = json.dumps(msg)
            return HttpResponse(msg,content_type='application/json')




'''机构首页详情'''
class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:3] #反向取course
        all_teachers = course_org.teacher_set.all()[:1]


        return render(request,'org-detail-homepage.html',{
            'current_page':current_page,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org':course_org,
            }
        )


'''课程详情'''
class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3] #反向取course
        return render(request,'org-detail-course.html',{
            'current_page': current_page,
            'all_courses': all_courses,
            'course_org':course_org,
            }
        )


'''课程讲师详情'''
class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request,'org-detail-teachers.html',{
            'current_page':current_page,
            'all_teachers': all_teachers,
            'course_org':course_org,
            }
        )


'''机构详情'''
class OrgDescView(View):
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request,'org-detail-homepage.html',{
            'current_page':current_page,
            'course_org':course_org,
            }
        )


'''用户收藏和取消收藏ajax'''
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)         # 防止后边int(fav_id)时出错
        fav_type = request.POST.get('fav_type', 0)     # 防止int(fav_type)出错

        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            # 如果记录已经存在，表示用户取消收藏
            exist_record.delete()
            #目标收藏数要减一
            if int(fav_type) == 1 :
                course = Course.objects.get(id = int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id = int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id = int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"fail", "msg":"已取消收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                #收藏之后，目标收藏数要加一

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()


                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


'''讲师列表'''
class TeacherListView(View):
    def get(self,request):
        all_teachers = Teacher.objects.all()

        #全局搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = Teacher.objects.filter(Q(name__icontains=search_keywords)|Q(org__name__icontains=search_keywords)|Q(work_company__icontains=search_keywords))

        all_teachers_num = all_teachers.count()
        hot_teachers = all_teachers.order_by('-fav_nums')#人气排行

        rank_teachers = hot_teachers[:3]  #讲师排行榜

        #人气排行
        sort = request.GET.get("sort","")
        if sort == 'hot':
            all_teachers = hot_teachers


        #分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # 这里指从 all_teachers 中取出来，每页显示3个
        p = Paginator(all_teachers, 3, request=request)
        teachers = p.page(page)  #

        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'all_teachers_num':all_teachers_num,
            'sort':sort,
            'rank_teachers':rank_teachers,

        })



'''讲师详情'''
class TeacherDetail(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))  #获取讲师
        teacher.click_nums += 1
        teacher.save()
        courses = Course.objects.filter(teacher_id = int(teacher_id)) #该讲师的课程
        belong_org = CourseOrg.objects.get(teacher = teacher) #该讲师所属机构
        rank_teachers = Teacher.objects.all().order_by('-fav_nums')


        #分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # 这里指从 courses 中取出来，每页显示3个
        p = Paginator(courses, 3, request=request)
        courses = p.page(page)  #

        # 教师收藏和机构收藏
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True



        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'courses':courses,
            'belong_org':belong_org,
            'rank_teachers': rank_teachers,
            'has_org_faved':has_org_faved,
            'has_teacher_faved':has_teacher_faved,
        })

