# Generated by Django 2.1 on 2019-02-27 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_worker_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='employer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='user',
            name='detail',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='enterprise',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
        migrations.AddField(
            model_name='user',
            name='price',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.ImageField(blank=True, choices=[(0, '男'), (1, '女')], null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='user',
            name='skill',
            field=models.ManyToManyField(blank=True, null=True, to='account.Skill', verbose_name='技能'),
        ),
        migrations.AddField(
            model_name='user',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='Employer',
        ),
        migrations.DeleteModel(
            name='Worker',
        ),
    ]