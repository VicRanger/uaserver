from django.urls import path

from . import views

app_name = 'ua'

urlpatterns = [
    path('signup',views.signup,name="signup"),
    path('user',views.user,name="user"),
    path('login',views.login,name="login"),
    path('send_phone',views.send_phone,name="send_phone"),
    path('check_phone',views.check_phone,name="check_phone"),
]
