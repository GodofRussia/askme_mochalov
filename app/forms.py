from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from . import models


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=5, widget=forms.PasswordInput)

    def clean_password(self):
        return self.cleaned_data["password"]


class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    nickname = forms.CharField()
    password = forms.CharField(min_length=5, widget=forms.PasswordInput)
    repeated_password = forms.CharField(min_length=5, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.Profile
        fields = ["username", "password", "email", "nickname", "avatar"]

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
        return models.Profile.objects.create(user=user, avatar=self.cleaned_data["avatar"], nickname=self.cleaned_data[
            "nickname"])


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    def save(self, user, question):
        return models.Answer.objects.create(profile=models.Profile.objects.get(user=user), question=question, text=self
                                            .cleaned_data["text"])
