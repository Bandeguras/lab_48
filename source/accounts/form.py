from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2',
                  'first_name']
        field_classes = {'username': UsernameField}
