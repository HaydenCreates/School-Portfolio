from .models import *
from django import forms
from django.db import models
from users.models import Profile


class PostForm(forms.ModelForm):
    title = models.CharField(max_length=200)
    content = models.TextField()
    attachment = models.FileField(upload_to='post_attachments/', blank=True, null=True)
    classNum = models.IntegerField()
    class Meta:
        model = Post
        fields = ['title', 'content', 'attachment', 'classNum']

class CommentForm(forms.ModelForm):
    content = forms.TextInput()
    classNum = forms.IntegerField(required=False)
    class Meta:
        model = Comment
        fields = ['content','user','post','classNum']

class TextLessonForm(forms.ModelForm):
    class Meta:
        model = TextLesson
        fields = ['title', 'content', 'classNum']

class QuizForm(forms.ModelForm):
    class Meta:
        model=Quiz
        fields=['title', 'classNum']

class QuestionForm(forms.ModelForm):
    class Meta:
        model= Question
        fields="__all__"

#ModelForm is used for the views form
class ClassForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.TextInput()
    classNum = forms.CharField(max_length=255)
    teacher = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Class
        fields =['name', 'description', 'classNum', 'teacher']

#form for the text lessons
class completeTextForm(forms.ModelForm):
    response = forms.CharField(widget=forms.TextInput())
    attachment = models.FileField(upload_to='post_attachments/', blank=True, null=True)
    class Meta:
        model = completeText
        fields = ['response','attachment']

