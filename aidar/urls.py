from django.contrib import admin
from django.urls import path
from blog.views import post_list, register, user_login, user_logout, switch_lang


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_list, name='home'),
    path('register/', register, name='register'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('lang/<str:lang>/', switch_lang, name='switch_lang'),
]