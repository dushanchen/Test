from django.db import models

# Create your models here.



class User(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '用户'

    nickname = models.CharField(max_length=100,verbose_name='用户昵称',null=True)
    avatar_url = models.CharField(max_length=200,verbose_name='用户头像',null=True)
    open_id = models.CharField(max_length=100,verbose_name='open_id',unique=True)

    name = models.CharField(max_length=20,verbose_name='姓名',null=True)
    city = models.CharField(max_length=20,verbose_name='城市',null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[(0,'启用'),(1,'禁用')],default=0)
    phone = models.CharField(max_length=20,null=True)




class Employer(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '包工'

    user = models.ForeignKey(User,on_delete=models.CASCADE)



class Worker(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '工人'

    user = models.ForeignKey(User,on_delete=models.CASCADE)