# Generated by Django 2.0.5 on 2018-10-09 11:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ua', '0002_user_is_phone_activated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_phone_activated',
            new_name='is_phone_verified',
        ),
        migrations.AddField(
            model_name='user',
            name='idcode',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='idcode_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='暂无用户名', max_length=64),
        ),
    ]
