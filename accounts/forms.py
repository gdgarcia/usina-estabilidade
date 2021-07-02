from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        # fields = UserCreationForm.Meta.fields + ('age',)
        # we dont need to set password. it is required
        fields = ('username', 'email', 'age',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        # fields = UserChangeForm.Meta.fields
        # we dont need to set password. it is required
        fields = ('username', 'email', 'age',)
