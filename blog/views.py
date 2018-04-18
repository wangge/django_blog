from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,Http404
from .models import Blog, Comment
import datetime
from .forms import CommentForm,LoginForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    """
    获取博客列表
    :param request:
    :return:
    """
    blog_list = Blog.objects.order_by('pub_date')[:10]
    content = {'blog_list':blog_list}
    return render(request, 'blog/index.html',content)

def detail(request, blog_id):
    """
    获取博客详情
    :param request:
    :param blog_id:
    :return:
    """
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/detail.html',{'blog':blog,'comment_form':CommentForm})

def comment(request, blog_id):
    post = CommentForm(request.POST)
    if not post.is_valid():##验证表单
        blog = get_object_or_404(Blog, pk=blog_id)
        return render(request, 'blog/detail.html',{'blog':blog,'error_message':post.errors})
    Comment.objects.create(blog_id=blog_id,comment_text=request.POST['comment'],comment_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return HttpResponse('comment OK')
@require_http_methods(['GET','POST'])
def login_blog(request):
    """
    用django认证系统登录
    :param request:
    :return:
    """
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('登录成功')
        else:
            return HttpResponse('登录失败')
    else:
        return render(request, 'blog/login.html', {'form': LoginForm})


@login_required(login_url='/blog/login/')
def logout_blog(request):
    """
    只有登录后的用户才能退出
    :param request:
    :return:
    """
    logout(request)
    return HttpResponse('退出成功')
