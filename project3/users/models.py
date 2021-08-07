from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
