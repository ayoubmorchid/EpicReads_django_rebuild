from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "category", "description", "image", "available"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password1 = forms.CharField(
        label="Password",
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Type your password",
                "autocomplete": "new-password",
            }
        ),
        error_messages={
            "min_length": "Password must be at least 6 characters.",
            "required": "Password is required.",
        },
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Confirm your password",
                "autocomplete": "new-password",
            }
        ),
        error_messages={"required": "Please confirm your password."},
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Type your username",
            "email": "Type your email address",
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "input",
                    "placeholder": placeholders.get(field_name, ""),
                }
            )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already used.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data.get("email", ""),
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Type your username or email",
                "autocomplete": "username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Type your password",
                "autocomplete": "current-password",
            }
        )
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct username/email and password. "
            "Both fields may be case-sensitive."
        ),
        "inactive": "This account is inactive.",
    }

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email is not None and password:
            username = username_or_email.strip()

            if "@" in username:
                matched_user = User.objects.filter(email__iexact=username).first()
                if matched_user:
                    username = matched_user.get_username()

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
