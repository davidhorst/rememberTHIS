from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MinLengthValidator
import datetime 
from .models import clean_date, clean_email

class UserCreateForm(UserCreationForm):
 
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name","password1", "password2")

    email = forms.EmailField(
        required=True,
        validators=[clean_email])
    first_name = forms.CharField(
        max_length=30, 
        validators=[MinLengthValidator(2)],
        error_messages={
            'min_length': ("First name must be longer than 2 characters")}
            )
    last_name = forms.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
        error_messages={
            'min_length': ("Last name must be longer than 2 characters")}
            )

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        # print user
        user.username = user.email

        if commit:
            user.save()
        return user

class UserUpdateForm(UserChangeForm):
 
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=30, 
        validators=[MinLengthValidator(2)],
        error_messages={
            'min_length': ("First name must be longer than 2 characters")}
            )
    last_name = forms.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
        error_messages={
            'min_length': ("Last name must be longer than 2 characters")}
            )

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user