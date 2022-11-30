from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import History


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password2:
                return password2
        raise forms.ValidationError("Invalid password")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Username contains special characters")

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Username already exists")

    def save(self):
        User.objects.create_user(
            username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])


class HistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, *kwargs)

    class Meta:
        model = History
        fields = ['body']


class UploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        'id': 'file_id'
    }))


class uploadform(forms.Form):
    image = forms.ImageField()
    text = forms.Textarea()
