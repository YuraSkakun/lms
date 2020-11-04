from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from user_account.models import UserAccountProfile


class UserAccountRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):  # <---- !!!!   .Meta
        # model = User
        fields = ("username", "first_name", "last_name", "email")

    """ unique email:"""
    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.all().filter(email=email).exists():    # or  .count()>0
            raise ValidationError('Email already exists')

        return email

    def clean(self):

        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        if first_name == last_name:
            raise ValidationError('First and Last name must be different')

        return self.cleaned_data


class UserAccountProfileForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.all().filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('Email already exists')

        return email


class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = UserAccountProfile
        fields = ['image']
