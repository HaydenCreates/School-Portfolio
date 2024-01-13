#holds links for the urls for each page
#calls a view
from django.urls import path
from users import views

urlpatterns = [

    #index is the name of the view's function
    path("", views.login_user, name="login"),
    path("login/", views.signUp_user, name="signup"),

    #logout
    path("logoutUser/", views.logout_user, name="logoutUser")
]
