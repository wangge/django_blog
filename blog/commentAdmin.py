from django.contrib import admin
from .models import Blog
from django.contrib.auth.decorators import permission_required
class CommentAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    ordering = ['comment_date']
    ####自定义显示列表
    fieldsets = (
        ['博客', {'fields': ['blog']}],
        ['评论', {'fields': ['comment_text']}],
        ['评论时间', {'fields': ['comment_date']}],
        ['审核状态', {'fields': ['valid']}],
    )
    list_display = ('blog', 'comment_text', 'comment_date','blog_comment','valid')
    def blog_comment(self, obj):
        return Blog.objects.get(title=obj.blog).content
    blog_comment.short_description = '博客内容'
    actions = ['delete_selected','make_valid']
    search_fields = ['blog__title','blog__content','comment_text','comment_date']  # 搜索字段
    #readonly_fields = ['blog','comment_text','comment_date']
    def make_valid(self, request, queryset):

        perm = request.user.has_perm('can_valid_comment')

        if not perm:
            self.message_user(request,"您没有审核权限")
            return
        rows_updated = queryset.update(valid='s')
        ##处理事件错误
        if rows_updated == 1:
            message_bit = '1 Comment was'
        else:
            message_bit = "%s Comments were " % rows_updated

        self.message_user(request ,"%s Succussfully marked as validated ." % message_bit)
    make_valid.short_description = "审核"
