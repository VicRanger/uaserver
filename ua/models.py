from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    login_time = models.DateTimeField(null=True)
    phone = models.CharField(max_length=32)
    password = models.CharField(max_length=512)
    raw_password = models.CharField(max_length=512)
    username = models.CharField(max_length=64, default="暂无用户名")
    nickname = models.CharField(max_length=64, default="暂无昵称")
    intro = models.CharField(max_length=256, default="暂无简介")
    email = models.CharField(max_length=265, default="暂无邮箱")
    is_phone_verified = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    idcode = models.CharField(max_length=10,default="")
    idcode_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.pk) + " " + self.phone


class Picture(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, editable=True)
    update_time = models.DateTimeField(auto_now=True, editable=True)
    key = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
