from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from .models import Post, Category, Comment

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email','password1','password2')

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type":"password"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type":"password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type":"password"}))
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_passwod2"]


class uploadform(forms.Form):
    image = forms.ImageField()
    text = forms.Textarea()

choices = list(Category.objects.all().values_list('name', 'name'))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=('title', 'author', 'category','body')
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control'}),
            'author': forms.TextInput(attrs={'class' : 'form-control', 'id':'name','type':'hidden'}),
            'category': forms.Select(choices=choices,attrs={'class' : 'form-control'}),
            'body': forms.Textarea(attrs={'class' : 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) :
        self.author = kwargs.pop('author', None)
        self.post = kwargs.pop('post', None)
        self.body = kwargs.pop('body', None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.body = self.body
        comment.author = self.author
        comment.post = self.post
        comment.save()
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class' : 'form-control'}),
        }

        

