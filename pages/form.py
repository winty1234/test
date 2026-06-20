import re

from .models import User, Application, Review

from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', "email", "full_name", "phone", "birth_date", "password1", "password2")

        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"})
        }

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        if len(username) < 6:
            raise forms.ValidationError("Логин должен содержать минимум 6 символов.")
        if not re.fullmatch(r"[A-Za-z0-9]+", username):
            raise forms.ValidationError("Логин должен содержать только латинские буквы и цифры.")
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name", "")
        if len(full_name.split()) < 2:
            raise forms.ValidationError("Полное имя должно содержать не меньше 2 слов.")
        return full_name


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("time_start", "transport", "payment_type")
        widgets = {
            "time_start": forms.DateInput(attrs={"type": "date"}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }