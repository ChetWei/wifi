# _*_ encoding:utf-8_*_
from django.db import models


from datetime import datetime
from organization.models import CourseOrg,Teacher

# Create your models here.


class Course(models.Model):
    DEGREE_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级"),
    )

    name = models.CharField("课程名",max_length=50)
    desc = models.CharField("课程描述",max_length=300)
    detail = models.TextField("课程详情")
    degree = models.CharField('难度',choices=DEGREE_CHOICES, max_length=2)
    learn_times = models.IntegerField("学习时长(分钟数)",default=0)
    students = models.IntegerField("学习人数",default=0)
    fav_nums = models.IntegerField("收藏人数",default=0)
    image = models.ImageField("封面图",upload_to="courses/%Y/%m",max_length=100)
    is_banner = models.BooleanField('是否轮播', default=False)
    click_nums = models.IntegerField("点击数",default=0)
    add_time = models.DateTimeField("添加时间",default=datetime.now,)
    course_org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name='所属机构',null=True,blank=True,default='')
    star = models.CharField('星级',max_length=2,default=5)
    category = models.CharField('课程类别',max_length=30,default='全栈开发')
    tag = models.CharField('课程标签',max_length=20,default='')
    teacher = models.ForeignKey(Teacher,null=True,blank=True,verbose_name="讲师",on_delete=models.CASCADE)
    need_know = models.CharField('课程须知',max_length=200,default='')
    learn_what = models.CharField('能学到什么',max_length=200,default='')

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name


        #获取课程的章节数
    def get_sum_lessons(self):
        return self.lesson_set.all().count()


        #获取这门课程的学习用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = '课程轮播图'
        verbose_name_plural = verbose_name
        proxy = True  #不会生成表，具有表的功能，为了让一张表注册两个管理器


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField("章节名",max_length=100)
    add_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)

    def get_all_video(self):
        return self.video_set.all()



class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节",on_delete=models.CASCADE)
    name = models.CharField("视频名",max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)
    url = models.URLField('视频地址',max_length=200,default='')
    learn_times = models.IntegerField("学习时长(分钟数)", default=0)


    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程",on_delete=models.CASCADE)
    name = models.CharField("名称",max_length=100)
    download = models.FileField("资源文件",upload_to="course/resource/%Y/%m",max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
