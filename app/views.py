import string

from django.contrib import auth
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from . import models
from . import forms
from .models import paginate


def index(request):
    try:
        questions = models.Question.objects
    except models.Question.DoesNotExist:
        raise Http404
    new_questions = questions.get_new_questions()
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    page_object = paginate(new_questions, page_number, 3)
    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    context = {
        'questions': page_object.object_list,
        'page_object': page_object,
        'top_tags': top_tags,
        'best_members': best_members
    }
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    question_item = get_object_or_404(models.Question, id=question_id)
    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    if request.method == "GET":
        answer_form = forms.AnswerForm()
    if request.method == 'POST':
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            if not request.user.is_anonymous:
                answer = answer_form.save(request.user, question_item)
                answer_count = models.Answer.objects.count()
                answers_per_page = 2
                page_object = paginate(question_item.answers.all(), answer_count / answers_per_page, answers_per_page)
                return redirect(reverse("question", kwargs={"question_id": question_id}) + f"?page={page_object.number}#contact")
            else:
                return HttpResponse("Please sign in to make an answer!")
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    page_object = paginate(question_item.answers.all(), page_number, 2)
    context = {
        'question': question_item,
        'answers': page_object.object_list,
        'page_object': page_object,
        'top_tags': top_tags,
        'best_members': best_members,
        'form': answer_form
    }
    return render(request, 'question.html', context=context)


def ask(request):
    return render(request, 'ask.html')


@csrf_protect
def login_user(request):
    if request.method == "GET":
        user_form = forms.LoginForm()
    if request.method == 'POST':
        user_form = forms.LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse("index"))
            else:
                user_form.add_error(field=None, error="Wrong username or password!")

    context = {'form': user_form}
    return render(request, 'login.html', context=context)


@csrf_protect
def signup(request):
    if request.method == "GET":
        user_form = forms.RegisterForm()
    if request.method == 'POST':
        user_form = forms.RegisterForm(request.POST)
        if user_form.is_valid():
            profile = user_form.save()
            if profile:
                return redirect(reverse("index"))
            else:
                user_form.add_error(field=None, error="Wrong user saving!")

    context = {'form': user_form}
    return render(request, 'signup.html', context=context)


def settings(request):
    return render(request, 'settings.html')


def logout(request):
    auth.logout(request)

    return redirect(reverse("index"))


def hot(request):
    try:
        questions = models.Question
    except models.Question.DoesNotExist:
        raise Http404
    top_questions = questions.objects.get_hot_questions()
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    page_object = paginate(top_questions, page_number, 3)
    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    context = {
        'questions': page_object.object_list,
        'page_object': page_object,
        'top_tags': top_tags,
        'best_members': best_members
    }

    return render(request, 'hot_questions.html', context=context)


def tag(request, tag_name: string):
    try:
        questions = models.Question
    except models.Question.DoesNotExist:
        raise Http404
    questions_by_tag = questions.objects.get_questions_by_tag(tag_name)
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    page_object = paginate(questions_by_tag, page_number, 3)
    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    context = {
        'questions': page_object.object_list,
        'tag_name': tag_name,
        'page_object': page_object,
        'top_tags': top_tags,
        'best_members': best_members
    }

    return render(request, 'questions_by_tag.html', context=context)
