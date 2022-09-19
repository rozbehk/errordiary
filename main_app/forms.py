from django.forms import ModelForm
from .models import Error,Comment

class ErrorForm(ModelForm):
  class Meta:
    model = Error
    fields = ['title', 'language','description', 'solution']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['text_input','date']