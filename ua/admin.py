from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ['Info',{
            'fields':('nickname','phone','email')
        }],
        ['Login',{
            'fields':('username','password'),
        }],
        ['Time',{
            'fields':('create_time', 'update_time','login_time',)
        }],
        ['Activation',{
            'fields':('is_phone_verified','is_activated',)
        }]
    )

admin.site.register(User,UserAdmin)