from django.db import models

# Create your models here.



class Skill(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '技能'

    name = models.CharField(max_length=20, verbose_name='技能名称')


class User(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '用户'

    nickname = models.CharField(max_length=100,verbose_name='用户昵称',null=True)
    avatar_url = models.CharField(max_length=200,verbose_name='用户头像',null=True)
    open_id = models.CharField(max_length=100,verbose_name='open_id',unique=True)

    name = models.CharField(max_length=20,verbose_name='姓名',null=True)
    city = models.CharField(max_length=20,verbose_name='城市',null=True)
    status = models.IntegerField(choices=[(0,'启用'),(1,'禁用')],default=0)
    type = models.IntegerField(choices=[(0,'包工'),(1,'工匠')], null=True)
    phone = models.CharField(max_length=20,null=True)
    show_phone = models.IntegerField(choices=[(0, '显示'),(1, '隐藏')], null=True, blank=True)
    enterprise = models.CharField(max_length=100, null=True, blank=True)
    price = models.ImageField(null=True, blank=True)
    detail = models.CharField(max_length=500, null=True, blank=True)
    sex = models.IntegerField(choices=[(0, '男'),(1, '女')], null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    icon = models.ImageField(upload_to='image', null=True, blank=True)
    skill = models.ManyToManyField('Skill', null=True, blank=True, verbose_name='技能')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField(null=True)
