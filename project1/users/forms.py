
from django import forms
from django.contrib.auth.models import User
from users.models import Class
from django.contrib.auth.forms import UserCreationForm

#login into the form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

#Sign up user
class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    user_type = forms.ChoiceField(choices=[('teacher','Teacher'), ('student', 'Student')])
    enrolled_classes = forms.ModelChoiceField(queryset=Class.objects.all(), empty_label="Teacher", required=False)

    class Meta:
        model = User
        fields = ('username', 'password1','password2','email',
                  'first_name', 'last_name', 'user_type','enrolled_classes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('classNum', 'name', 'description', 'teacher')
