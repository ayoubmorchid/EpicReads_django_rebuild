from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "category", "description", "image", "available"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username = self.cleaned_data.get("username")
        if username and "@" in username:
            user = User.objects.filter(email__iexact=username).first()
            if user:
                self.cleaned_data["username"] = user.get_username()
        return super().clean()
