from django.forms import ModelForm
from .models import Error, Comment, UserAvatar
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import date

class DateInput(forms.DateInput):
  input_type = 'date'
class ErrorForm(ModelForm):

  date = forms.DateField(widget=DateInput)
  class Meta:
    model = Error
    fields = ['title', 'language','description', 'solution', 'date']

  def __init__(self, *args, **kwargs):
    super(ErrorForm, self).__init__(*args, **kwargs)
    self.fields['title'].widget.attrs['class'] = 'form-control'
    self.fields['title'].widget.attrs['style'] = 'width:600px; height:40px;'
    self.fields['language'].widget.attrs['class'] = 'form-control'
    self.fields['description'].widget.attrs['class'] = 'form-control'
    self.fields['description'].widget.attrs['style'] = 'width:600px; height:100px;'
    self.fields['solution'].widget.attrs['class'] = 'form-control'
    self.fields['solution'].widget.attrs['style'] = 'width:600px; height:100px;'
    self.fields['solution'].required = False
    self.fields['date'].widget.attrs['class'] = 'form-control'
    self.fields['date'].widget.attrs['value'] = date.today()
    self.fields['date'].widget.attrs['disabled'] = True

class CommentForm(ModelForm):
  date = forms.DateField(widget=DateInput)
  class Meta:
    model = Comment
    fields = ['text_input','date']

  def __init__(self, *args, **kwargs):
    super(CommentForm, self).__init__(*args, **kwargs)
    self.fields['text_input'].widget.attrs['class'] = 'form-control'
    self.fields['date'].widget.attrs['class'] = 'form-control'
    self.fields['date'].widget.attrs['style'] = 'width:200px; height:40px;'
    self.fields['date'].widget.attrs['value'] = date.today()
    self.fields['date'].widget.attrs['disabled'] = True

class RegisterUserForm(UserCreationForm):
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
  first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

  def __init__(self, *args, **kwargs):
    super(RegisterUserForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].widget.attrs['class'] = 'form-control'

class UserUpdateForm(ModelForm):
  username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
  first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']

  def __init__(self, *args, **kwargs):
    super(UserUpdateForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['style'] = 'width:400px; height:40px;'