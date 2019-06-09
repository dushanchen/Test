# Generated by Django 2.1 on 2019-02-20 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='技能名称')),
            ],
            options={
                'verbose_name': '技能',
                'verbose_name_plural': '技能',
            },
        ),
        migrations.AddField(
            model_name='employer',
            name='age',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='employer',
            name='enterprise',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='age',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='worker',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
        migrations.AddField(
            model_name='worker',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='price',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='employer',
            name='skill',
            field=models.ManyToManyField(blank=True, null=True, to='account.Skill', verbose_name='技能'),
        ),
        migrations.AddField(
            model_name='worker',
            name='skill',
            field=models.ManyToManyField(blank=True, null=True, to='account.Skill', verbose_name='技能'),
        ),
    ]