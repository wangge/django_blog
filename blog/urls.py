from django.urls import path

from . import views

#给路由添加命名空间,用法blog:index
app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:blog_id>/',views.detail,name='detail'),
    path('<int:blog_id>/comment/',views.comment,name='comment'),
    path('login/',views.login_blog,name='login'),
    path('logout/',views.logout_blog,name='logout')
]