from django import forms
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
        # , "nickname", "avatar"
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
        user = models.User.objects.create(username=self.username, password=self.password, email=self.email)
        return models.Profile.objects.create(user_id=user, avatar=self.avatar, nickname=self.nickname)


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

