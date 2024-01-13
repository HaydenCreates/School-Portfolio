from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from decimal import Decimal

# Create your views here.
def home(request):
    user = request.user
    # Find the class associated with the student
    if user.is_authenticated:
        if request.user.groups.filter(name='Teacher').exists():
            user_class = Class.objects.filter(teachers=user).first()
        else:
            user_class = Class.objects.filter(students=user).first()

        posts = Post.objects.filter(classNum=user_class).order_by('-created_at')
        return render(request, "index.html", {'posts': posts})
    else:
        posts = Post.objects.none()
    return render(request, "index.html",{'posts': posts})

#logout User
@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    messages.success(request,message="Logout Successful")
    return redirect("home")

@login_required(login_url='/login/')
#allows sudents to view results
def view_results(request):
    # Get the currently logged-in student
    user = request.user  # Assuming the user is logged in

    # Find the class associated with the student - for multiple use a dictionary to iterate through each?
    isTeacher = user.profile.user_type

    text =[]
    multiple =[]

    teach = isTeacher == "teacher"
    if teach:
        class_instance = Class.objects.filter(teacher=user)

        #have an input that can then change the weight based on the input (new url)

        for currClass in class_instance:
            textResult = completeText.objects.filter(classNum = currClass)
            text.append({'class': currClass, 'results': textResult})

            quiz = Quiz.objects.filter(classNum=currClass)
            quizResult = Grade.objects.filter(quiz__in=quiz)
            multiple.append({'class': currClass, 'results': quizResult})


    else:
        class_instance = Class.objects.filter(students = user)
        for currClass in class_instance:

            #gets the final results for each course
            finalResult = FinalGrade.objects.filter(course=currClass, student=user).first()

            #gets current users Text grades for a class
            textResult = completeText.objects.filter(classNum = currClass, user=user)
            text.append({'class': currClass, 'results': textResult, 'letter': finalResult})

            #gets current users Quiz grades for a class
            quiz = Quiz.objects.filter(classNum=currClass)

            #gets all grades and orders the grades
            for quizzes in quiz:

                #gets all the students in one class
                quizResult = Grade.objects.filter(quiz=quizzes, student=user)
                userGrade = Grade.objects.filter(quiz=quizzes, student=user).order_by("-grade", 'submissions').first()
                allStudents = currClass.students.all()
                lower = 0
                totalGrades = 0

                print(currClass.name)

                #gets the last submissions of each student
                for studentIn in allStudents:
                    otherGrades =  Grade.objects.filter(quiz=quizzes,student=studentIn).order_by("-grade", 'submissions').first()
                    if otherGrades is not None:
                        print(otherGrades.student)
                        print(otherGrades.grade)
                        totalGrades += 1
                        print(otherGrades.quiz)
                        print(totalGrades)

                        #counts how many are lower than student's grade - exclusive method
                        try:
                            if userGrade.grade is not None and otherGrades.student != user and otherGrades.grade < userGrade.grade:
                                lower += 1
                                print(lower)
                        except:
                            break

                #gets the pecentile
                try:
                    percentileCal = (lower/totalGrades) * 100
                    print("percentile: ")
                    print(percentileCal)

                except ZeroDivisionError:
                    print("None Type")
                    percentileCal = 'None'

                multiple.append({'class': currClass, 'results': quizResult, 'percent': percentileCal, 'letter': finalResult})

    return render(request, 'Results.html', {'text':text, 'multiple': multiple, 'teacher': teach})

#use app to plot graphs - need a new page to show?
#Sort the scores based on criteria
@login_required(login_url='/login/')
def sortResult(request):
    # Get the currently logged-in student
    user = request.user  # Assuming the user is logged in

    # Find the class associated with the teaher
    isTeacher = user.profile.user_type

    #if using dropdown get rid of this - condense to one
    text = []
    multiple = []
    average = False
    iterable = True

    #need highest, lowest, and average scores
    if request.method == 'POST':
        sortOption = request.POST.get("sortSelect")

        teach = isTeacher == "teacher"
        if teach:

            class_instance = Class.objects.filter(teacher=user)
            for currClass in class_instance:
                #checks if option is selected
                if request.POST:
                    #Highest to Lowest
                    if(sortOption == '1'):
                        #highest first
                        textDescend = completeText.objects.filter(classNum = currClass).order_by('-grade')
                        text.append({'class': currClass, 'results': textDescend})

                        quiz = Quiz.objects.filter(classNum=currClass)
                        quizDesend = Grade.objects.filter(quiz__in=quiz).order_by("-grade")
                        multiple.append({'class': currClass, 'results': quizDesend})

                        print("High to Low")

                    #Lowest to Highest
                    elif(sortOption == '2'):

                        textAscend = completeText.objects.filter(classNum = currClass).order_by('grade')
                        text.append({'class': currClass, 'results': textAscend})

                        quiz = Quiz.objects.filter(classNum=currClass)
                        quizAscend = Grade.objects.filter(quiz__in=quiz).order_by("grade")
                        multiple.append({'class': currClass, 'results': quizAscend})

                        print("Low to High")

                    #Highest Score - make it show if have multiple similar ones
                    elif(sortOption == '3'):
                        print("Highest Score")

                        textDescend = completeText.objects.filter(classNum = currClass).order_by('-grade').first()
                        text.append({'class': currClass, 'results': textDescend})

                        quiz = Quiz.objects.filter(classNum=currClass)
                        quizDesend = Grade.objects.filter(quiz__in=quiz).order_by("-grade").first()
                        multiple.append({'class': currClass, 'results': quizDesend})
                        iterable = False

                    #Lowest score - make it show if have multiple similar ones
                    elif(sortOption == '4'):
                        print("Lowest Score")

                        textAscend = completeText.objects.filter(classNum = currClass).order_by('grade').first()
                        text.append({'class': currClass, 'results': textAscend})

                        quiz = Quiz.objects.filter(classNum=currClass)
                        quizAscend = Grade.objects.filter(quiz__in=quiz).order_by("grade").first()
                        multiple.append({'class': currClass, 'results': quizAscend})
                        iterable = False

                    #Average score
                    elif(sortOption == '5'):
                        print("Average")

                        # Calculate average for completeText
                        textScores = completeText.objects.filter(classNum=currClass).values_list('grade', flat=True)
                        textScores = [score for score in textScores if score is not None]
                        textAverage = sum(textScores) / len(textScores) if len(textScores) > 0 else None
                       # Get the lesson title
                        lessonTitle = TextLesson.objects.filter(classNum=currClass).values_list('title', flat=True).first()

                        text.append({'class': currClass, 'lesson_title': lessonTitle, 'results': textAverage})

                        # Calculate average for Quiz
                        quizScores = Grade.objects.filter(quiz__classNum=currClass).values_list('grade', flat=True)
                        quizScores = [score for score in quizScores if score is not None]
                        quizAverage = sum(quizScores) / len(quizScores) if len(quizScores) > 0 else None
                        # Get the quiz name
                        quizName = Quiz.objects.filter(classNum=currClass).values_list('title', flat=True).first()

                        multiple.append({'class': currClass, 'quiz_name': quizName, 'results': quizAverage})

                        average = True
                        iterable = False
        else:
            print("Not Valid")

            #get the button pressed and select the ascending or decending based on that? - use dropdown select?

    return render(request, 'sortedResults.html', {'text':text, 'multiple': multiple, 'teacher': teach, 'average': average, 'iterable': iterable})

# creates a post - have to be logged in
@login_required(login_url='/login/')
def create_post(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_classes = user.enrolled_classes.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            #if there are no files to save
            if not request.FILES.get('attachment'):
                form.instance.attachment = None

            # Save the post with the attached file - make it use multiple files
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('allLessons')
        else:
            print(form.errors)
    else:
        form = PostForm()
        print(form.errors)
    return render(request, 'createPost.html', {'form': form, 'user_classes': user_classes})

#creates a lesson
@permission_required('users.can_view_all', login_url='/login/')
def createLesson(request):
    return render(request, 'createLesson.html', {})

#creates a text lesson - add replies to it for the grading?
@permission_required('users.can_view_all', login_url='/login/')
def createTextLesson(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_classes = user.enrolled_classes.all()
    if request.method == 'POST':
        form = TextLessonForm(request.POST, request.FILES)
        if form.is_valid():
            #if there are no files to save
            if not request.FILES.get('attachment'):
                form.instance.attachment = None

            # Save the post with the attached file - make it use multiple files
            post = form.save(commit=False)
            post.author = request.user
            post.semester = request.POST['semester']
            post.save()
            return redirect('allLessons')
        else:
            print(form.errors)
    else:
        form = TextLessonForm()
        print(form.errors)
    return render(request, 'textLesson.html', {'form': form, 'user_classes': user_classes})

#creates a multiple choice lesson
@permission_required('users.can_view_all', login_url='/login/')
@login_required(login_url='/login/')
def createChoiceLesson(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_classes = user.enrolled_classes.all()
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
         # Save the question first
            save = form.save(commit=False)

            save.title = form.cleaned_data['title']
            save.semester = request.POST['semester']
            save.author = user

            #Take the info from this to make a questions that go into quiz object
            save.save()

            # Redirect to a success page or another URL
            return redirect('allLessons')
        else:
            print(form.errors)
    else:
        form= QuizForm()
    return render(request,'multipleLesson.html',{'form': form, 'user_classes': user_classes})

#Add a question to the quiz
@login_required(login_url='/login/')
def addQuestion(request, uuid):
    user_id = request.user
    lesson = get_object_or_404(Quiz, id=uuid)
    questions = Question.objects.filter(quiz=lesson)

    is_teacher =  request.user.profile.user_type
    if is_teacher == 'teacher':
        user_class = True
    else:
        user_class = False  # Or any other default value

    #may need to fix this
    previous_submission = Grade.objects.filter(student=user_id, quiz=lesson).order_by('-submissions').first()

    #if the user has done all attempts or has gotten a 100 then it close off
    if (previous_submission is not None and previous_submission.submissions >= 3) or previous_submission.grade == 100.00:
        print(previous_submission.submissions)
        messages.warning(request, 'You have already submitted this lesson.')
        return redirect('allLessons')
    else:

        #grading system
        if request.method == "POST":
            #one for making the questions
            form1 = QuestionForm(request.POST)

            if form1.is_valid():
                quest = form1.save(commit= False)
                quest.save()

            if 'submit' in request.POST:

                print("grading")
                total_questions = len(questions)
                correct = 0
                for question in questions:

                    selected_answer_str = request.POST.get(str(question.id))
                    if selected_answer_str is not None:
                        try:
                            selected_answer = int(selected_answer_str)
                        except ValueError:
                            selected_answer = None
                        if selected_answer == question.ans:
                            correct += 1

                    try:
                        total = correct/total_questions * 100
                    except ZeroDivisionError:
                        total = 0.00

                #for the other submissions models
                if previous_submission is None or previous_submission.submissions is None:
                    grade = Grade.objects.create(
                        grade = total,
                        quiz=lesson,
                        student=request.user,
                        submissions = 1
                    )

                    grade.save()
                else:
                    print("changing the thing" + str(total))
                    grade = Grade.objects.create(
                        grade = total,
                        quiz=lesson,
                        student = request.user,
                        submissions = previous_submission.submissions + 1
                    )

                    grade.save()

                return redirect('allLessons')
            else:
                print("not graded")

        else:
            form1 = QuestionForm()
    return render(request, 'multiple_lesson_detail.html', {'form1':form1, 'lesson':lesson, 'questions':questions, 'user_class': user_class})

#shows all the posts
@login_required(login_url='/login/')
def allPost(request):
    user = request.user
    posts = []
    # Find the class associated with the student
    if request.user.groups.filter(name='Teacher').exists():
        user_class = Class.objects.filter(teachers=user)
    else:
        user_class = Class.objects.filter(students=user)

    for currClass in user_class:
        post_content = Post.objects.filter(classNum =currClass).order_by('-created_at')  # Query all posts from the database
        posts.append({'class': currClass, 'results': post_content})

    comments = Comment.objects.all()

    return render(request, 'allPost.html', {'posts':posts, 'comments':comments})

#shows all the lessons
@login_required(login_url='/login/')
def allLessons(request):
   # Get the currently logged-in student
    user = request.user  # Assuming the user is logged in
    text=[]
    multiple =[]

    # Find the class associated with the student - need to change later
    if request.user.groups.filter(name='Teacher').exists():
        user_class = Class.objects.filter(teachers=user)
    else:
        user_class = Class.objects.filter(students=user)

    # one for the text and one for the multiple choice
    # Get assignments for the student's class
    for currClass in user_class:
        text_content = TextLesson.objects.filter(classNum=currClass)
        text.append({'class': currClass, 'results': text_content})

        multiple_content = Quiz.objects.filter(classNum=currClass)
        multiple.append({'class': currClass, 'results': multiple_content})

    return render(request, 'allLessons.html', {'multiple': multiple, 'text': text})

#Teacher adds classes
@permission_required('users.can_view_all', login_url='/login/')
@login_required(login_url='/login/')
def addClass(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():

            new_class = form.save(commit=False)  # Create but don't save yet
            new_class.save()  # Now save the instance
            new_class.students.add(request.user)

            messages.success(request, 'Class created successfully')
            return redirect('home')
        else:
            messages.error(request, 'Class creation failed. Please check your input.')
    else:
        form = ClassForm()
        print(form.errors)

    return render(request, 'addClass.html', {'form':form})

#adds a comment to a post
def addComment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            print("Comment saved")
            return HttpResponseRedirect(reverse('allPost'))
        else:
            print(form.errors)
    else:
        form = CommentForm()
        print(form.errors)

    return render(request, 'allPost.html', {'form': form})

#one for text and one for multiple choice?
@permission_required('users.can_view_individual', login_url='/login/')
@login_required(login_url='/login/')
#lets the student take the quiz
def lesson_detail(request, lesson_id, uuid):
    try:
        text_lesson = TextLesson.objects.get(id=lesson_id)
        return render(request, 'text_lesson_detail.html', {'lesson': text_lesson})
    except TextLesson.DoesNotExist:
        pass  # Handle if it's not a text lesson

    try:
        multiple_lesson = Quiz.objects.get(uuid=uuid)
        return render(request, 'multiple_lesson_detail.html', {'lesson': multiple_lesson})
    except Quiz.DoesNotExist:
        pass  # Handle if it's not a quiz

    # Handle if the lesson doesn't exist or is of an unknown type
    return HttpResponseNotFound("Lesson not found")

#student fills out the text lesson - need to be 3 submissions?
def completeTextIn(request, lesson_id):
    user_id = request.user
    lesson = get_object_or_404(TextLesson, id=lesson_id)
    classNum = lesson.classNum

    previous_submission = completeText.objects.filter(user=user_id).first()
    if previous_submission is not None and previous_submission.submissions >= 3:
        messages.warning(request, 'You have already submitted this lesson.')
        return redirect('allLessons')
    else:
        if request.method == 'POST':
            form = completeTextForm(request.POST, request.FILES)
            print(classNum)
            if form.is_valid():
                if previous_submission is None or previous_submission.submissions is None:
                    #if there are no files to save
                    if not request.FILES.get('attachment'):
                        form.instance.attachment = None

                    # Save the post with the attached file - make it use multiple files
                    answer = form.save(commit=False)
                    answer.classNum = classNum
                    answer.lesson = lesson
                    answer.user = user_id
                    answer.submissions = 1
                    answer.save()
                else:
                    previous_submission.response = request.POST.get('response')

                    if not request.FILES.get('attachment'):
                        previous_submission.attachment = None
                    else:
                        previous_submission.attachment = request.FILES.get('attachment')

                    previous_submission.submissions += 1

                    previous_submission.save()
                return redirect(reverse('allLessons'))
            else:
                print(form.errors)
        else:
            form = completeTextForm()
            print(form.errors)
    return render(request, 'text_lesson_detail.html',{'form': form, 'lesson': lesson, 'classNum': classNum})

#adds students to classes that the teacher creates
@permission_required('users.can_view_all', login_url='/login/')
@login_required(login_url='/login/')
def addStudent(request):
    teach_Classes = Class.objects.filter(teacher = request.user)
    student = Profile.objects.filter(user_type = 'student')

    if request.method == "POST":
        selected_class_id = request.POST.get('classNum')

        selected_students = request.POST.getlist('students')

        selected_class = Class.objects.get(classNum = selected_class_id)

        for student in selected_students:
            print("usernne: " + student)
            user = User.objects.get(username=student)
            if user not in selected_class.students.all():
                profile = Profile.objects.get(user=user, user_type = 'student')
                selected_class.students.add(user)
                profile.enrolled_classes.add(selected_class)
                redirect('allPost')
            else:
                print("student is already in class: " + user)

    return render(request, 'addStudent.html', {'teach_Classes':teach_Classes, 'student':student})

#shows the search results
@login_required(login_url='/login/')
def searchResult(request):
    posts=[]
    text=[]
    quiz =[]
    if request.method == 'POST':
        user = request.user
        if request.user.groups.filter(name='Teacher').exists():
            user_class = Class.objects.filter(teachers=user)
        else:
            user_class = Class.objects.filter(students=user)

        comments = Comment.objects.all()

        for currClass in user_class:
            searched = request.POST.get('searched')
            posts_content = Post.objects.filter(title__icontains= searched, classNum= currClass)
            posts.append({'class': currClass, 'results': posts_content})

            text_content = TextLesson.objects.filter(title__icontains=searched,  classNum= currClass)
            text.append({'class': currClass, 'results': text_content})

            quiz_content = Quiz.objects.filter(title__icontains= searched,  classNum= currClass)
            quiz.append({'class': currClass, 'results': quiz_content})

    return render(request, 'searchResult.html', {'searched':searched, 'posts':posts,
                                                 'text':text, 'quiz':quiz, 'comments':comments})

#change grades for student
def changeGrade(request, completetext_id):
    # Get the completeText instance by its ID
    complete_text_instance = get_object_or_404(completeText, id=completetext_id)

    if request.method == 'POST':
        # Handle form submission for updating the grade
        new_grade = request.POST.get('newGrade')
        try:
            new_grade = Decimal(new_grade)
        except ValueError:
            print("still str")
            redirect('Results.html')

        if new_grade <= 100.00 or new_grade >= 0.00:
            complete_text_instance.grade = new_grade
            complete_text_instance.save()
            return HttpResponseRedirect(reverse('results'))
        else:
            redirect('Results.html')
        # Redirect to a success page or do other processing
    return render(request,'Results.html', {'complete_text_instance': complete_text_instance})

#change the weight for lesson
def changeTextWeight(request, completetext_id):
    complete_text_instance = get_object_or_404(completeText, id=completetext_id)

    if request.method == 'POST':
        # Handle form submission for updating the grade
        new_weight = request.POST.get('newTextWeight')
        try:
            new_weight = Decimal(new_weight)
        except ValueError:
            print("still str")
            redirect('Results.html')

        text_instance = complete_text_instance.lesson
        text_instance.weight = new_weight
        text_instance.save()
        HttpResponseRedirect('Results.html')

    return render(request,'Results.html', {'text_instance': text_instance})

#change the weight for Quiz
def changeQuizWeight(request, quiz_id):
    quizMain = get_object_or_404(Grade, id=quiz_id)

    if request.method == 'POST':
        # Handle form submission for updating the grade
        new_weight = request.POST.get('newQuizWeight')
        print(new_weight)
        try:
            new_weight = Decimal(new_weight)
        except ValueError:
            print("still str")
            HttpResponseRedirect('Results.html')

        quiz_instance = quizMain.quiz
        quiz_instance.weight = new_weight
        quiz_instance.save()

        HttpResponseRedirect('Results.html')

    return render(request,'Results.html', {'quiz_instance': quiz_instance})

#creates the chart for the teachers to view
@permission_required('users.can_view_all', login_url='/login/')
@login_required(login_url='/login/')
def chart(request):
    # Get the currently logged-in student
    user = request.user  # Assuming the user is logged in

    chart_labels = []
    chart_data = []

    class_instance = Class.objects.filter(teacher=user)

    #have an input that can then change the weight based on the input (new url)

    for currClass in class_instance:
        textResult = completeText.objects.filter(classNum = currClass)
        quiz = Quiz.objects.filter(classNum=currClass)
        quizResult = Grade.objects.filter(quiz__in=quiz)

        semester_scores = {}

        #scores for the quizes
        for result in quizResult:
            semester = result.quiz.semester
            if semester not in semester_scores:
                semester_scores[semester] = []

            semester_scores[semester].append(result.grade)

        #scores for text lessons
        for result in textResult:
            semester = result.lesson.semester
            if semester not in semester_scores:
                semester_scores[semester] = []

            semester_scores[semester].append(result.grade)

        for semester, scores in semester_scores.items():
            class_label = f"{currClass.name} - Semester {semester}"
            non_none_scores = [score for score in scores if score is not None]

            if non_none_scores:  # Check if there are non-None scores to avoid division by zero
                chart_labels.append(class_label)
                chart_data.append(sum(non_none_scores) / len(non_none_scores))
            else:
                # Handle the case where all scores are None (or an empty list)
                chart_labels.append(class_label)
                chart_data.append(0)  # or any default value you prefer

        chart_data = [float(value) if value is not None else None for value in chart_data]

        print(chart_labels)

    return render(request,'charts.html', {'chart_labels': chart_labels, 'chart_data': chart_data})

#computes the letter grades for the students
@permission_required('users.can_view_all', login_url='/login/')
@login_required(login_url='/login/')
def calculateLetter(request):
    user = request.user

    class_instance = Class.objects.filter(teacher=user)
    totalGrade = []
    chart_data = []
    chart_labels = []

    for currClass in class_instance:
        allStudents = currClass.students.all()

        #gets current users Quizs and lessons for a class
        quiz = Quiz.objects.filter(classNum=currClass)
        lessons = TextLesson.objects.filter(classNum=currClass)

        #gets the last quiz submissions of each student
        for studentIn in allStudents:
            totalOfGrades = 0
            letter = ''
            allWeight = []
            if studentIn.profile.user_type != "teacher":
                #gets all quiz grades and orders the grades
                for quizzes in quiz:
                    quizGrades =  Grade.objects.filter(quiz=quizzes,student=studentIn).order_by("-grade", 'submissions').first()
                    if quizGrades is not None:
                        if quizGrades.grade is not None:
                            totalOfGrades += (float(quizzes.weight)/100) * int(quizGrades.grade)
                        else:
                            totalOfGrades += 0

                    else:
                        print("No quiz")

                    allWeight.append(quizzes.weight)

                #gets all lesson grades for each students
                for sub in lessons:
                    textGrades =  completeText.objects.filter(lesson=sub,user=studentIn).order_by("-grade", 'submissions').first()
                    if textGrades is not None:
                        if textGrades.grade is None:
                            totalOfGrades += 0
                        else:
                            totalOfGrades += (float(sub.weight)/100) * int(textGrades.grade)

                    else:
                        totalOfGrades += 0

                    allWeight.append(sub.weight)

                try:
                    total =  totalOfGrades / sum(allWeight)
                except ZeroDivisionError:
                    total = 0


                #Creates a letter grade based on the weighted average
                if total >= .90 and (total <= 1.00 or total > 1.00):
                    letter =='A'
                elif total <= .89 and total >= .80:
                    letter = 'B'
                elif total <= .79 and total >= .70:
                    letter = 'C'
                elif total <= .69 and total >= .60:
                    letter = 'D'
                else:
                    letter = 'F'

                #Creates or updates the Grade
                studFinal = FinalGrade.objects.filter(course=currClass, student=studentIn).first()

                if studFinal is None:
                    final = FinalGrade.objects.create(
                        final_grade = letter,
                        student = studentIn,
                        course = currClass,
                    )

                    final.save()
                else:
                    studFinal.final_grade = letter
                    studFinal.save()

                #adds to the list of total weighted grades per student
                totalGrade.append({'student': studentIn, 'weighted': total, 'class': currClass, 'final':letter})

            else:
                print("teacher")
                pass

        chart_labels.append(f'A - {currClass.name}')
        chart_data.append(FinalGrade.objects.filter(course=currClass, final_grade= 'A').count())
        chart_labels.append(f'B - {currClass.name}')
        chart_data.append(FinalGrade.objects.filter(course=currClass, final_grade= 'B').count())
        chart_labels.append(f'C - {currClass.name}')
        chart_data.append(FinalGrade.objects.filter(course=currClass, final_grade= 'C').count())
        chart_labels.append(f'D - {currClass.name}')
        chart_data.append(FinalGrade.objects.filter(course=currClass, final_grade= 'D').count())
        chart_labels.append(f'F - {currClass.name}')
        chart_data.append(FinalGrade.objects.filter(course=currClass, final_grade= 'F').count())


    return render(request,'letters.html', {'allGrades': totalGrade, 'chart_labels': chart_labels, 'chart_data': chart_data})
