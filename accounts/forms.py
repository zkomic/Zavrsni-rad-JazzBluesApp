from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from JazzBluesApp.models import Users, GENDER_CHOICES

class registrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

class addFields(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    avatar = forms.ImageField(required=False)
    class Meta:
        model = Users
        fields = ("gender", "avatar",)
        


