from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Error, Comment,Screenshot
from .forms import CommentForm,ErrorForm



class ErrorCreate(CreateView):
  model = Error
  fields = ['title', 'language','description', 'solution','date']

class ErrorUpdate(UpdateView):
  model = Error
  fields = ['title', 'language','description', 'solution','date']

class ErrorDelete(DeleteView):
  model = Error
  success_url = '/errors/'

def home(request):
  errors = Error.objects.all()
  return render(request, 'home.html', { 'errors': errors })

def about(request):
  return render(request, 'about.html')

def errors_index(request):
  errors = Error.objects.all()
  return render(request, 'errors/index.html', { 'errors': errors })

def errors_detail(request, error_id):
  error = Error.objects.get(id=error_id)
  comment_form = CommentForm()
  return render(request, 'errors/detail.html', {
    'error': error, 
    'comment_form': comment_form,
  })

def add_comment(request, error_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.error_id = error_id
    new_comment.save()
  return redirect('error_detail', error_id=error_id)
