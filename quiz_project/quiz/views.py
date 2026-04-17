from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'home.html', {'quizzes': quizzes})


@login_required(login_url='login')
def create_quiz(request):
    form = QuizForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        quiz = form.save(commit=False)
        quiz.created_by = request.user
        quiz.save()
        return redirect('add_question', quiz.id)

    return render(request, 'create_quiz.html', {'form': form})


@login_required(login_url='login')
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuestionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        return redirect('add_choice', question.id)

    return render(request, 'add_question.html', {'form': form, 'quiz': quiz})


@login_required(login_url='login')
def add_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    form = ChoiceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        choice = form.save(commit=False)
        choice.question = question
        choice.save()
        return redirect('add_choice', question.id)

    return render(request, 'add_choice.html', {'form': form, 'question': question})


def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices').all()
    score = None
    total = questions.count()

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_choice_id = request.POST.get(f'q{question.id}')
            if selected_choice_id:
                if question.choices.filter(id=selected_choice_id, is_correct=True).exists():
                    score += 1

    return render(request, 'start_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'score': score,
        'total': total,
    })