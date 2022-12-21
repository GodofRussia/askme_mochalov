import string

from django.contrib import auth
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
    page_object = paginate(new_questions, request, 3)
    top_tags = models.Tag.objects.get_top_tags
    context = {
        'questions': page_object.object_list,
        'page_object': page_object,
        'top_tags': top_tags
    }
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    question_item = get_object_or_404(models.Question, id=question_id)
    page_object = paginate(question_item.answers.all(), request, 2)
    top_tags = models.Tag.objects.get_top_tags
    context = {
        'question': question_item,
        'answers': page_object.object_list,
        'page_object': page_object,
        'top_tags': top_tags
    }
    return render(request, 'question.html', context=context)


def ask(request):
    return render(request, 'ask.html')


@csrf_protect
def login(request):
    if request.method == "GET":
        user_form = forms.LoginForm()
    if request.method == 'POST':
        user_form = forms.LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
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
    page_object = paginate(top_questions, request, 3)
    top_tags = models.Tag.objects.get_top_tags
    context = {
        'questions': page_object.object_list,
        'page_object': page_object,
        'top_tags': top_tags
    }

    return render(request, 'hot_questions.html', context=context)


def tag(request, tag_name: string):
    try:
        questions = models.Question
    except models.Question.DoesNotExist:
        raise Http404
    questions_by_tag = questions.objects.get_questions_by_tag(tag_name)
    page_object = paginate(questions_by_tag, request, 3)
    top_tags = models.Tag.objects.get_top_tags
    context = {
        'questions': page_object.object_list,
        'tag_name': tag_name,
        'page_object': page_object,
        'top_tags': top_tags
    }

    return render(request, 'questions_by_tag.html', context=context)
