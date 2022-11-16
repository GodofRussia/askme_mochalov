from django.contrib.auth.models import User
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

# Create your models here.

Questions = [
    {
        'id': question_id,
        'title': 'title' + str(question_id),
        'text': 'text' + str(question_id),
        'answers_count': question_id * question_id,
        'tags': [
            {
                'id': tag_id,
                'tag_name_': 'tag' + str(tag_id),
            } for tag_id in range(3*question_id)
        ],
        'answers': [
            {
                'id': answer_id,
                'text': 'answer text' + str(answer_id),
            } for answer_id in range(question_id * question_id)
        ]
    } for question_id in range(20)
]


def find_questions(tag_name):
    questions = []
    for question_item in Questions:
        tags = question_item.get('tags')
        for tag_item in tags:
            if tag_item.get('tag_name_').__contains__(tag_name) and not questions.__contains__(question_item):
                questions.append(question_item)

    return questions


def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_object = p.get_page(page_number)

    return page_object


class QuestionModelManager(models.Manager):
    def get_hot_questions(self):
        rating_set = self.rating_set.all()
        general_rating = 0
        for rating in rating_set:
            if rating.value:
                general_rating += 1
            else:
                general_rating -= 1

        return self.filter(self.all().order_by(general_rating))

    def get_new_questions(self):
        return self.filter(self.all().order_by('creation_date'))


class Profile(models.Model):
    login = models.CharField(max_length=30, null=True, blank=True)
    nick_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)


class TagManager(models.Manager):
    def get_questions_by_tag(self):
        return Question.objects.filter(tag=self)


class Tag(models.Model):
    tag_name = models.CharField(max_length=10)
    objects = TagManager


class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=200)
    creation_date = models.DateField(null=True, blank=True)
    tag = models.ManyToManyField(Tag)
    objects = QuestionModelManager
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(max_length=200)
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT, null=True, blank=True)
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)


class Rating(models.Model):
    value = models.BooleanField()
    is_question_rating = models.BooleanField()
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT, null=True, blank=True)
    answer_id = models.ForeignKey(Answer, on_delete=models.PROTECT, null=True, blank=True)
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=Q(is_question_rating=True),
                fields=["question_id"],
                name="unique_question"
            ),
            models.UniqueConstraint(
                condition=Q(is_question_rating=False),
                fields=["answer_id"],
                name="unique_answer"
            )
        ]
