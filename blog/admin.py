from django.contrib import admin

# Register your models here.
from .models import Blog,Comment
from django.http import HttpRequest as request
from django.db.models.query import QuerySet as queryset

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from .commentAdmin import CommentAdmin

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

#评论的审核权限
#content_type = ContentType.objects.get_for_model(Comment)
#permission = Permission.objects.create(
#    codename='can_valid',
#    name='Can Valid Comments',
#    content_type=content_type
#)
#def make_published(admin, request, queryset):
# #   queryset.update('status=p')
#make_published.short_description = 'Mark selected Blogs as published'

##动作事件--导出(全局)
def export_selected_objects(admin, request, queryset):
    selected = request.POST.getlist(admin.ModelAdmin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

class BlogAdmin(admin.ModelAdmin):

    date_hierarchy = 'pub_date' ## date_hierachy = blog__pub_date
    empty_value_display = "-empty-"
    ordering = ['pub_date']
    ####自定义显示列表
    fieldsets = (
        ['标题',{'fields':['title']}],
        ['内容',{'fields':['content']}],
        ['发布时间',{'fields':['pub_date']}],
        ['状态',{'fields':['status'],'description':'编辑页面的描述'}]
    )

    list_display = ('title','content','pub_date','status','other_field')
    list_display_links = ['title','content']  #那些字段有链接,默认情况是list_display第一个
    list_editable = ['pub_date','status'] #可以在列表编辑的选项
    #筛选
    list_filter = ['title','pub_date','status'] #如果不是该模块的字段，可以用夸关系查找，model__filter,comment__comment_text,相信见https://docs.djangoproject.com/zh-hans/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter

    list_max_show_all = 1000 #最多显示条数
    list_per_page = 10
    #select_related 关联关系
    #save_on_top = True
    search_fields = ['title','content'] #搜索字段
    show_full_result_count = True
    def other_field(self, obj):
        return '您好'
    other_field.short_description = "自定义选项"
    other_field.admin_order_field = 'title' ##告诉ａｄｍｉｎ用那个字段排序
    readonly_fields = ['status'] ##编辑页面只读的字段
    ### 动作事件
    actions = ['make_published']
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        ##处理事件错误
        if rows_updated == 1:
            message_bit = '1 Blogs was'
        else:
            message_bit = "%s Blogs were " % rows_updated

        self.message_user(request ,"%s Succussfully marked as published ." % message_bit)
    make_published.short_description = "Mark selected Blogs as published"

    actions_on_top = False ##是否在顶部显示action,默认True
    actions_on_bottom = True ##是否在底部显示action　默认False


admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.add_action(export_selected_objects,'导出')##全局的action
admin.site.disable_action('delete_selected') ##使删除action功能失效