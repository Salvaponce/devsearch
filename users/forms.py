from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fiels = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name' : 'name'
        }