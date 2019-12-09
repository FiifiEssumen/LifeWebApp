from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from Slife.models import Comment, Contact

class LoginForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=PasswordInput)

class RegisterForm(UserCreationForm):
# (forms.Form)
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email Already Exists')
        return email
    class Meta:
            model = User
            fields = ["username","email","password1"]

class CommentForm(forms.ModelForm):
     class Meta:
         model = Comment     
         fields = ['comment']


class ContactForm(forms.ModelForm):
      class Meta:
          model = Contact
          fields = ['name','email','subject','message']                   