from django import forms

class CommentForm(forms.Form):
    """
    创建一个评论的表单
    """
    comment = forms.CharField(label='评论',required=True,error_messages={'required':'not ok'})

class LoginForm(forms.Form):
    """
    一个登录Ｆｏｒｍ
    """
    username = forms.CharField(label='用户名',required=True)
    password = forms.CharField(label='密码',required=True, widget=forms.PasswordInput)