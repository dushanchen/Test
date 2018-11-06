from django.db import models

# Create your models here.


class Tender(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '招标信息'

    province = models.CharField(max_length=10,verbose_name='省份')
    id = models.CharField(max_length=50,primary_key=True,verbose_name='id')
    title = models.CharField(max_length=100,verbose_name='标题')
    content = models.TextField(null=True,verbose_name='内容')
    source_url = models.CharField(max_length=200,default='',verbose_name='原文链接')
    publish_time = models.DateTimeField(null=True,verbose_name='发布时间')

    def __str__(self):
        return self.title



class Log(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '爬取日志'

    create_time = models.DateTimeField(auto_now_add=True,verbose_name='爬取时间')
    count = models.IntegerField(verbose_name='总数')
    lose = models.IntegerField(verbose_name='失败')
    success = models.IntegerField(verbose_name='成功')
    province = models.CharField(max_length=20,verbose_name='省份')
    a_type = models.CharField(max_length=10,verbose_name='大类型')

    def __str__(self):
        return '__'.join([self.create_time.strftime('%Y-%m-%d %H:%M:%S'),self.province,self.a_type,str(self.count),str(self.success),str(self.lose)])