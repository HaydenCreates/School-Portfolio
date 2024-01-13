# Create your models here.
from django.db import models
from users.models import Class
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class TextLesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    classNum = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    semester = models.IntegerField(null=True)

    #weight for the lesson
    weight = models.FloatField(default=1.0)

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    classNum = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    semester = models.IntegerField(null=True)

    #weight per quiz
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question_text = models.CharField(max_length=200, null=True)
    opt1 = models.CharField(max_length=100, null=True)
    opt2 = models.CharField(max_length=100, null=True)
    opt3 = models.CharField(max_length=100, null=True)
    opt4 = models.CharField(max_length=100, null=True)
    ans = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], null=True)

    def __str__(self):
        if self.quiz is not None and self.quiz.title is not None:
            return self.quiz.title
        return "Question without Quiz Title"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='post_attachments/', blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    classNum = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)

    # Method to increment view count - use somewhere
    def increment_views(self):
        self.views_count += 1
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Assuming you have a Post model
    classNum = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

class completeText(models.Model):
    lesson = models.ForeignKey(TextLesson, on_delete=models.CASCADE, null=True)
    response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='post_attachments/', blank=True, null=True)
    classNum = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    #optional for later
    submissions = models.IntegerField(default=0)

    def __str__(self):
        return f'Response by {self.user} on {self.classNum}'


class Grade(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    submissions = models.IntegerField(default=0)

    def __str__(self):
        return self.quiz.title

class FinalGrade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Class, on_delete=models.CASCADE)  # Assuming Class is the model for your courses
    final_grade = models.CharField(max_length=2)
