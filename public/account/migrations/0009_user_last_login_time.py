# Generated by Django 2.1 on 2019-02-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_user_show_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login_time',
            field=models.DateTimeField(null=True),
        ),
    ]