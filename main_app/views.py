from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Error, Comment,Screenshot
from .forms import CommentForm,ErrorForm, RegisterUserForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class ErrorCreate(LoginRequiredMixin, CreateView):
  model = Error

  form_class = ErrorForm
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ErrorUpdate(LoginRequiredMixin, UpdateView):
  model = Error
  fields = ['title', 'language','description', 'solution','date']

class ErrorDelete(LoginRequiredMixin, DeleteView):
  model = Error
  success_url = '/errors/'

def home(request):
  errors = Error.objects.all()
  return render(request, 'home.html', { 'errors': errors })

def about(request):
  return render(request, 'about.html')

@login_required
def errors_index(request):
  errors = Error.objects.filter(user=request.user)
  return render(request, 'errors/index.html', { 'errors': errors })

@login_required
def errors_detail(request, error_id):
  error = Error.objects.get(id=error_id)
  comment_form = CommentForm()
  return render(request, 'errors/detail.html', {
    'error': error, 
    'comment_form': comment_form,
  })

@login_required
def add_comment(request, error_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.error_id = error_id
    new_comment.save()
  return redirect('error_detail', error_id=error_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = RegisterUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = RegisterUserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def search(request):
  if request.method == 'GET':       
      title =  request.GET.get('search')      
      errors = Error.objects.filter(title__icontains=title)
      return render(request,"errors/search_results.html",{"errors":errors})
  else:
      return render(request,"errors/search_results.html",{})
def user_profile(request):
  errors = Error.objects.filter(user_id = request.user.id)
  return render(request, 'home.html', { 'errors': errors })