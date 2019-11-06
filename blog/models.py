from django.db import models

STATUS_CHOICES = (
    ('d','草稿'),#Draft
    ('p','已发布'),#Published
    ('w','撤销'),#withdrawn
)
# Create your models here.
class Blog(models.Model):
    title = models.CharField('标题',max_length=200)
    content = models.TextField('内容',max_length=255)
    pub_date = models.DateTimeField('发布时间')
    status = models.CharField('状态',max_length=1,choices=STATUS_CHOICES,default='d')

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog , on_delete=models.CASCADE)
    comment_text = models.CharField('评论',max_length=200)
    comment_date = models.DateTimeField('评论时间')
    valid = models.CharField('审核状态',max_length=1,choices=(('u','未审核'),('s','已审核'),('f','驳回')),default='u')
    class Meta:
        permissions = (("can_valid_comment", "Can validation comment"),)#新增权限设置
    def __str__(self):
        return self.comment_text

