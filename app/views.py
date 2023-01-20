import string
import json

from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST
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
        raise HttpResponseBadRequest
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
                page_number = ((models.Answer.objects.filter(question=question_item).count() + 1) // 2)
                return redirect(reverse("question", kwargs={"question_id": question_id}) + f"?page={page_number}#contact")
            else:
                return HttpResponse("Please sign in to make an answer!")
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise HttpResponseBadRequest
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


@login_required(login_url='login', redirect_field_name="continue")
def ask(request):
    if request.method == "GET":
        question_form = forms.QuestionForm()
    if request.method == "POST":
        question_form = forms.QuestionForm(request.POST)
        if question_form.is_valid():
            if not request.user.is_anonymous:
                new_question = question_form.save(request.user)
                return redirect(reverse("question", kwargs={"question_id": new_question.id}))
            else:
                return HttpResponse("Please sign in to make an answer!")

    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    context = {
        'top_tags': top_tags,
        'best_members': best_members,
        'form': question_form
    }
    return render(request, 'ask.html', context=context)


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
                next = request.POST.get('continue', '/')
                return HttpResponseRedirect(next)
            else:
                user_form.add_error(field=None, error="Wrong username or password!")

    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    context = {
        'form': user_form,
        'top_tags': top_tags,
        'best_members': best_members,
    }
    return render(request, 'login.html', context=context)


@csrf_protect
def signup(request):
    if request.method == "GET":
        user_form = forms.RegisterForm()
    if request.method == 'POST':
        user_form = forms.RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            profile = user_form.save()
            if profile:
                login(request, profile.user)
                return redirect(reverse("index"))
            else:
                user_form.add_error(field=None, error="Wrong user saving!")

    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    context = {
        'form': user_form,
        'top_tags': top_tags,
        'best_members': best_members,
    }
    return render(request, 'signup.html', context=context)


@login_required(login_url='login',redirect_field_name="continue")
def settings(request):
    if request.method == 'GET':
        user = model_to_dict(request.user)
        user_form = forms.SettingsForm(initial=user)
        user_form.set_nickname(user)
    if request.method == 'POST':
        user_form = forms.SettingsForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        return HttpResponseRedirect(reverse('settings'))
    top_tags = models.Tag.objects.get_top_tags
    best_members = models.Profile.objects.get_top_members()
    context = {
        'top_tags': top_tags,
        'best_members': best_members,
        'form': user_form
    }
    return render(request, 'settings.html', context=context)


@login_required(login_url='login', redirect_field_name="continue")
def logout(request):
    auth.logout(request)
    url = request.GET.get('continue', '/')

    return redirect(url)


def hot(request):
    try:
        questions = models.Question
    except models.Question.DoesNotExist:
        raise Http404
    top_questions = questions.objects.get_hot_questions()
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise HttpResponseBadRequest
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
        raise HttpResponseBadRequest
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


@login_required
@require_POST
def like(request):
    data = json.loads(request.body.decode())
    type = data['type']
    id = data['id']
    is_question = data['is_question']
    if is_question == "True":
        question_item = models.Question.objects.get(id=id)
        try:
            question_item.questionRatings.get(profile=request.user.profile)
        except models.QuestionRating.DoesNotExist:
            if type == 'like':
                question_item.rating += 1
                value = True
            else:
                question_item.rating -= 1
                value = False

            question_like = models.QuestionRating.objects.create(question=question_item, profile=request.user.profile,
                                                                 value=value)
            question_item.save()
            question_like.save()
            return JsonResponse({
                "status": "ok",
                'likes_count': question_item.rating,
            })
    else:
        answer_item = models.Answer.objects.get(id=id)
        try:
            answer_item.answerRatings.get(profile=request.user.profile)
        except models.AnswerRating.DoesNotExist:
            if type == 'like':
                answer_item.rating += 1
                value = True
            else:
                answer_item.rating -= 1
                value = False

            answer_like = models.AnswerRating.objects.create(answer=answer_item, profile=request.user.profile,
                                                                 value=value)
            answer_item.save()
            answer_like.save()
            return JsonResponse({
                "status": "ok",
                'likes_count': answer_item.rating,
            })

    return JsonResponse({
        "status": "error",
        "message": "You've already made a rating"
    })


@login_required
@require_POST
def make_correct(request):
    data = json.loads(request.body.decode())
    question_id = data['question_id']
    answer_id = data['answer_id']
    status = data['status']
    answers = models.Answer.objects.filter(question_id=question_id).all()
    has_correct_answer = False
    for answer in answers:
        if answer.id != answer_id and answer.is_correct:
            has_correct_answer = True
    if has_correct_answer:
        return JsonResponse({
            "status": "error",
            "message": "You've already chosen a right answer"
        })
    answer = models.Answer.objects.get(id=answer_id)
    if not status:
        answer.is_correct = False
    else:
        answer.is_correct = True
    answer.save()
    return JsonResponse({
            "status": "ok",
            "answer_status": answer.is_correct
        })
