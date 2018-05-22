from django.db import models


from datetime import datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField('城市',max_length=20)
    desc = models.CharField('描述',max_length=200)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='操作时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural= verbose_name

    def __str__(self):
        return self.name
        
        
        
        
class CourseOrg(models.Model):
    name = models.CharField('机构名称',max_length=50)
    desc = models.TextField('机构描述')
    catgory = models.CharField(default='pxjg',max_length=30,choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')),verbose_name='机构类别')
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    students = models.IntegerField('学习人数',default=0)
    course_nums = models.IntegerField('课程数', default=0)
    image = models.ImageField('封面图',upload_to='org/%Y%m',max_length=100)
    address = models.CharField('机构地址',max_length=150,)
    city = models.ForeignKey(CityDict,verbose_name='所在城市',on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='操作时间')
    degree = models.CharField('名誉',default='全国知名',max_length=20)


    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

        

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name='所属机构',on_delete=models.CASCADE)
    name = models.CharField('教师名',max_length=50)
    work_years = models.IntegerField('工作年限',default=0)
    years_old  = models.IntegerField('年龄',default=0)
    work_company = models.CharField('就职公司',max_length=50)
    work_position = models.CharField('公司职位',max_length=50)
    degree = models.CharField('教学职称',max_length=20,default='')
    points = models.CharField('教学特点',max_length=50)
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='操作时间')
    pic = models.ImageField('头像',upload_to='teacher/%Y%m',max_length=100,default='default.jpg')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的教师: {1}".format(self.org, self.name)

    def get_course_nums(self):
        return self.course_set.all().count()