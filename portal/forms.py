from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, candidate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate is not None:
            self.fields["first_name"].initial = candidate.first_name
            self.fields["last_name"].initial = candidate.last_name
            self.fields["full_name"].initial = candidate.full_name
            self.fields["qualification"].initial = candidate.qualification
            self.fields["experience"].initial = candidate.experience
            self.fields["city"].initial = candidate.city
            self.fields["zip_code"].initial = candidate.zip_code
            if candidate.resume:
                self.fields["resume"].initial = candidate.resume.fileno

    class Meta:
        model = Candidate
        exclude = ['email', 'phone', 'details', 'user', 'email_confirmed']
