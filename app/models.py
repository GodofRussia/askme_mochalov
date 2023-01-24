from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse

from django.db.models import Q, Count
from django.utils import timezone


# Create your models here.


def paginate(objects_list, page_number, per_page=10):
    paginator = Paginator(objects_list, per_page)
    try:
        page_object = paginator.get_page(page_number)
    except EmptyPage:
        page_object = paginator.get_page(paginator.num_pages)
    return page_object


class AnswerModelManager(models.Manager):
    def get_hot_answer(self):
        return self.order_by('-rating')


class QuestionModelManager(models.Manager):
    def get_hot_questions(self):
        return self.order_by('-rating')

    def get_new_questions(self):
        new_questions = self.order_by('-creation_date')
        return new_questions

    def get_questions_by_tag(self, tag_name):
        return self.filter(tag__tag_name=tag_name)


class ProfileModelManager(models.Manager):
    def get_top_members(self):
        return self.annotate(q_count=(Count('questions') + Count('answers'))).order_by('-q_count')[:9]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(default='anonymous_avatar.png', upload_to='avatar/img/%Y/%m/%d/')
    objects = ProfileModelManager()

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def get_top_tags(self):
        return self.annotate(q_count=Count('questions')).order_by('-q_count')[:9]


class Tag(models.Model):
    tag_name = models.CharField(max_length=25)
    objects = TagManager()

    def __str__(self):
        return self.tag_name


class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=200)
    creation_date = models.DateField(default=timezone.now().time())
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="questions")
    tag = models.ManyToManyField(Tag, blank=True, related_name="questions")
    objects = QuestionModelManager()
    rating = models.IntegerField(default=0)

    def get_tags(self):
        return self.tag.all()

    def get_answers_count(self):
        return self.answers.count()

    def get_url(self):
        return reverse("question", kwargs={"question_id": self.id})

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    objects = AnswerModelManager()


class QuestionRating(models.Model):
    value = models.BooleanField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="questionRatings")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questionRatings")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "profile"],
                name="unique_question"
            )
        ]


class AnswerRating(models.Model):
    value = models.BooleanField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answerRatings")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answerRatings")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['answer', 'profile'],
                name="unique_answer"
            )
        ]
