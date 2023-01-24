import random
import string

from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from . import models


class LoginForm(forms.Form):
    username = forms.CharField(label='Login', help_text='Enter your login here')
    password = forms.CharField(label='Password', min_length=5, widget=forms.PasswordInput)

    def clean_password(self):
        return self.cleaned_data["password"]


class RegisterForm(forms.ModelForm):
    nickname = forms.CharField(label='Nickname')
    password = forms.CharField(min_length=5, widget=forms.PasswordInput)
    repeated_password = forms.CharField(min_length=5, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ["username", "password", "email"]

    def clean(self):
        password_1 = self.cleaned_data["password"]
        password_2 = self.cleaned_data["repeated_password"]

        if password_1 != password_2:
            raise ValidationError("Passwords do not match!?!")

        return self.cleaned_data

    def save(self, commit=True):
        self.cleaned_data.pop("repeated_password")
        user = models.User.objects.create(username=self.cleaned_data["username"], password=make_password(
            self.cleaned_data["password"]), email=self.cleaned_data["email"])
        if self.cleaned_data["avatar"] is None:
            return models.Profile.objects.create(user=user, nickname=self.cleaned_data["nickname"])

        return models.Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'], nickname=self.cleaned_data[
            "nickname"])


class AnswerForm(forms.Form):
    text = forms.CharField(label='Text of an answer', help_text='Type your answer here!', widget=forms.Textarea,
                           max_length=250)

    def save(self, user, question):
        return models.Answer.objects.create(profile=models.Profile.objects.get(user=user), question=question, text=self
                                            .cleaned_data["text"])


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=50, label='Question title')
    text = forms.CharField(widget=forms.Textarea, label='Question text', help_text='Describe your question',
                           max_length=250)
    tags = forms.CharField(label='Enter tags')

    def save(self, user):
        question = models.Question.objects.create(title=self.cleaned_data['title'], text=self.cleaned_data['text'],
                                                  profile=models.Profile.objects.get(user=user))
        tag_names = self.cleaned_data['tags']
        tag_list = tag_names.split(', ')
        for tag_name in tag_list:
            tag = models.Tag.objects.get_or_create(tag_name=tag_name)
            question.tag.add(tag[0])

        return question


class SettingsForm(forms.ModelForm):
    nickname = forms.CharField()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ['username', 'email']

    def set_nickname(self, user):
        profile = models.Profile.objects.get(user_id=user['id'])
        self.nickname = profile.nickname
        self.initial.update({'nickname': profile.nickname})

    def save(self, commit=True):
        user = super().save()
        profile = user.profile
        if self.cleaned_data["avatar"] is None:
            avatar = user.profile.avatar
        else:
            avatar = self.cleaned_data["avatar"]
        profile.avatar = avatar
        profile.nickname = self.cleaned_data['nickname']
        profile.save()

        return user
