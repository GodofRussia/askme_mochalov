import string

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from . import models
from .models import find_questions, paginate


def index(request):
    page_object = paginate(models.Questions, request, 3)
    context = {
        'questions': page_object.object_list,
        'page_object': page_object
    }
    return render(request, 'index.html', context=context)


def base(request):
    return render(request, 'base.html')


def question(request, question_id: int):
    question_item = models.Questions[question_id]
    page_object = paginate(question_item.get('answers'), request, 2)
    context = {
        'question': question_item,
        'answers': page_object.object_list,
        'page_object': paginate(question_item.get('answers'), request, 2)
    }
    return render(request, 'question.html', context=context)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    return render(request, 'hot_questions.html')


def tag(request, tag_name: string):
    questions = find_questions(tag_name)
    page_object = paginate(questions, request, 3)
    context = {
        'questions': page_object.object_list,
        'tag_name': tag_name,
        'page_object': page_object
        }

    return render(request, 'questions_by_tag.html', context=context)
