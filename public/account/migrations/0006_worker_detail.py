# Generated by Django 2.1 on 2019-02-24 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_worker_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='detail',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]