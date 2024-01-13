from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Permission
from .forms import LoginForm, SignUpForm
from .models import *

# Create your views here.
#login user
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            userName = form.cleaned_data["username"]
            passWord = form.cleaned_data["password"]

            user = authenticate(request, username=userName, password=passWord)
            if user is not None:
                login(request,user)
                print("Logged In")
                return redirect("home")
            else:
                print("Invalid Login")
                messages.error(request, message="Invalid username or password")

        else:
            print("Invalid Form")
            messages.error(request, message="Invalid Form Submission")
    else:
        print("Not Post")
        form = LoginForm()

    return render(request, 'login.html', {"form": form})

#create user
def signUp_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            userName = form.cleaned_data["username"]
            passWord = form.cleaned_data["password1"]
            user_type = form.cleaned_data["user_type"]
            selected_class =form.cleaned_data["enrolled_classes"]

            user = authenticate(request, username=userName, password=passWord)
            profile = Profile.objects.create(user=user, user_type=user_type)
            print("Signed Up")

            # Assign custom permissions based on user_type
            if user_type == 'teacher':
                permission = Permission.objects.get(codename='can_view_all')
                profile.user.user_permissions.add(permission)
            elif user_type == 'student':
                permission = Permission.objects.get(codename='can_view_individual')
                profile.user.user_permissions.add(permission)

            if selected_class:
                selected_class.students.add(user)
                profile.enrolled_classes.add(selected_class)

            login(request, user)
            messages.success(request,message="Resgistration Successful")
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = SignUpForm()
        print(form.errors)

    return render(request, 'signUp.html', {"form": form})


@login_required(login_url='/login/')
#logout User
def logout_user(request):
    logout(request)
    messages.success(request,message="Logout Successful")
    return redirect("home")
