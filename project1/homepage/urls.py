from django.urls import path
from homepage import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    #index is the name of the view's function - is the postlist so that it can load the posts
    path("home/", views.home, name="home"),

    #logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/home/'), name='logout'),

    #Create posts
    path('createPost/', views.create_post, name="createPost"),
    path('allLessons/', views.allLessons, name='allLessons'),
    path('allPost/', views.allPost, name='allPost'),
    path('results/', views.view_results, name='results'),
    path('allPost/<int:post_id>/', views.addComment, name='allPost'),
    path('choiceLesson/', views.createChoiceLesson, name='choiceLesson'),
    path('addClass/', views.addClass, name="addClass"),
    path('addStudent/', views.addStudent, name="addStudent"),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('completeText/<int:lesson_id>/', views.completeTextIn, name='completeText'),
    path('quizLesson/<uuid:uuid>/', views.addQuestion, name='quizLesson'),
    path('searchResult/', views.searchResult, name="searchResult"),
    path('results/<int:completetext_id>/', views.changeGrade, name='change_grade'),
    path('results-changeWeight/<int:completetext_id>/', views.changeTextWeight, name='change_text_weight'),
    path('results-changeQuizWeight/<int:quiz_id>/', views.changeQuizWeight, name='change_quiz_weight'),
    path('sortedresults/', views.sortResult, name='sortedresults'),
    path('chart/', views.chart, name='chart'),
    path('letters/', views.calculateLetter, name='letters'),
]
