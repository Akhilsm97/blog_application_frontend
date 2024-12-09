from django import forms
from . models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = UsersDetails
        fields = '__all__'


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = '__all__'

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
