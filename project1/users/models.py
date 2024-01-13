from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    classNum = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField(User, related_name='enrolled_classes', blank=True)

    def __str__(self):
        return self.name

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=30,choices=[('teacher','Teacher'), ('student', 'Student')])
    enrolled_classes = models.ManyToManyField(Class, blank=True)

    def __str__(self):
        return str(self.user)
