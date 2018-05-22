from django.shortcuts import render,HttpResponse
from django.views import View
from django.contrib.auth import authenticate,login  #登录
from django.db.models import Q

from user.models import UserProfile
from .models import Course,CourseOrg,Lesson,Video,CourseResource
from operation.models import CourseComments
from operation.models import UserFavorite,UserCourse
from pure_pagination import PageNotAnInteger,EmptyPage,Paginator #分页模块
from utils.mixin_utils import LoginRequiredMixin  #是否登录验证父类，跳转
# Create your views here.


def test(request):
    return render(request, 'course-comment.html')





'''课程列表'''
class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time') #默认按时间顺序

        hot_courses = Course.objects.all().order_by('-click_nums')[0:3] #取出热门课程，点击数排序
        #排序
        sort = request.GET.get('sort','')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort== 'hot':
            all_courses = all_courses.order_by('-click_nums')

        course_num = all_courses.count()


        #全局搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__contains=search_keywords)|Q(detail=search_keywords))


        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 这里指从 all_courses 中取五个出来，每页显示6个
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)  #

        return render(request,'course-list.html',{
            'all_courses':courses,
            'course_num':course_num,
            'sort': sort,
            'hot_courses':hot_courses,
        })


'''课程详情,收藏'''
class CourseDetailView(View):
    def get(self,request,course_id):

        current_course = Course.objects.get(id = course_id) #通过传递进来的id找到课程对象
        current_course.click_nums += 1   #当前课程的点击人数加一
        current_course.save()
        relate = Course.objects.filter(tag=current_course.tag)  # 获取相关的课程对象集合
        if relate:
            relate_courses = relate.order_by('-students')[:2]  # 2个
        else:
            relate_courses = []  # 因为这是一个前端遍历对象，所以空的时候要为数组类型，不然会报错
        current_course.click_nums += 1  # 增加课程点击数
        current_course.save()

        #判断用户是否收藏该课程以及热门机构
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:

            if UserFavorite.objects.filter(user=request.user, fav_id=current_course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=current_course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request,'course-detail.html',{
            'course':current_course,
            'relative_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org' : has_fav_org,
        })


'''课程章节学习'''
class CourseInfoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        current_course = Course.objects.get(id = course_id)#获取当前课程对象
        current_course.students += 1 #学习人数加一
        current_course.save()
        all_course_resource = CourseResource.objects.filter(course=current_course) #获取当前课程的所有资源
        all_lessons = current_course.lesson_set.all()  #获取当前课程的所有章节
        current_user = request.user
        sum_lessons = all_lessons.count() #计算章节数

        #学了这门课的同学还学了
        usercourse_objs = UserCourse.objects.filter(course=current_course) #找到学习了这门课的所有用户课程对象
        user_ids = [usercourse_obj.user_id for usercourse_obj in usercourse_objs] #遍历每个用户课程对象，获取所有用户id
        all_usercourse_objs = UserCourse.objects.filter(user_id__in=user_ids) #通过集合，在用户课程对象表中找到用户id在筛选范围内的用户课程对象
        #取出课程id
        course_ids = [all_usercourse_obj.course_id  for all_usercourse_obj in all_usercourse_objs]
        #取出相关课程
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request,'course-video.html',{
            'course':current_course,
            'lessons':all_lessons,
            'all_course_resource':all_course_resource,
            'relate_courses':relate_course,
        })



'''课程评论区'''
class CourseCommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):

        current_course = Course.objects.get(id=course_id)

        comments_objs = current_course.coursecomments_set.all().order_by('-add_time') #获取该课程的所有评论对象

        return render(request, 'course-comment.html', {
            'course':current_course,
            'comments_objs':comments_objs[:5],
        })



'''发表评论ajax处理'''
#添加评论
class AddCommentsView(View):
    '''用户评论'''
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse("{'status':'fail', 'msg':'用户未登录'}", content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            # 获取评论的是哪门课程
            course = Course.objects.get(id = int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()

            return HttpResponse("{'status':'success', 'msg':'评论成功'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'评论失败'}", content_type='application/json')



'''章节视频播放'''

class CoursePlayView(View):
    def get(self,request,vedio_id):
        vedio_obj = Video.objects.get(id=int(vedio_id))
        current_course  = Course.objects.get(id =vedio_obj.lesson.course_id)         #获取当前课程对象
        all_course_resource = CourseResource.objects.filter(course=current_course) #获取当前课程的所有资源
        all_lessons = current_course.lesson_set.all()  #获取当前课程的所有章节
        current_user = request.user
        sum_lessons = all_lessons.count() #计算章节数

        #学了这门课的同学还学了
        usercourse_objs = UserCourse.objects.filter(course=current_course) #找到学习了这门课的所有用户课程对象
        user_ids = [usercourse_obj.user_id for usercourse_obj in usercourse_objs] #遍历每个用户课程对象，获取所有用户id
        all_usercourse_objs = UserCourse.objects.filter(user_id__in=user_ids) #通过集合，在用户课程对象表中找到用户id在筛选范围内的用户课程对象
        #取出课程id
        course_ids = [all_usercourse_obj.course_id  for all_usercourse_obj in all_usercourse_objs]
        #取出相关课程
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request,'course-play.html',{
            'course':current_course,
            'lessons':all_lessons,
            'all_course_resource':all_course_resource,
            'relate_courses':relate_course,
            'vedio_obj':vedio_obj,
        })










