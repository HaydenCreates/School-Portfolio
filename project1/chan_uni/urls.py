"""
URL configuration for chan_uni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views
from homepage import views as homeViews

urlpatterns = [
    #references the links from the app's urls
    path("login/", include("users.urls")),
    path("studentsign/", include('django.contrib.auth.urls')),
    path("signup/", views.signUp_user, name="signup"),
    path("", include("homepage.urls")),
    path("createPost/", homeViews.create_post, name="createPost"),
    path('allLessons/', homeViews.allLessons, name='allLessons'),
    path('createLesson/', homeViews.createLesson, name='createLesson'),
    path('textLesson/', homeViews.createTextLesson, name='textLesson'),
    path('choiceLesson/', homeViews.createChoiceLesson, name='choiceLesson'),
    path('allPost/', homeViews.allPost, name='allPost'),
    path('results/', homeViews.view_results, name='results'),
    path('allPost/<int:post_id>/', homeViews.addComment, name='allPost'),
    path('addClass/', homeViews.addClass, name="addClass"),
    path('addStudent/', homeViews.addStudent, name="addStudent"),
    path('lessons/<int:lesson_id>/', homeViews.lesson_detail, name='lesson_detail'),
    path('completeText/<int:lesson_id>/', homeViews.completeTextIn, name='completeText'),
    path('quizLesson/<uuid:uuid>/', homeViews.addQuestion, name='quizLesson'),
    path('searchResult/', homeViews.searchResult, name='searchResult'),
    path('results/<int:completetext_id>/', homeViews.changeGrade, name='change_grade'),
    path('results-changeWeight/<int:completetext_id>/', homeViews.changeTextWeight, name='change_text_weight'),
    path('results-changeQuizWeight/<int:quiz_id>/', homeViews.changeQuizWeight, name='change_quiz_weight'),
    path('sortedresults/', homeViews.sortResult, name='sortedresults'),
    path('chart/', homeViews.chart, name='chart'),
    path('letters', homeViews.calculateLetter, name='letters'),
    path('admin/', admin.site.urls),
]
