from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Error, Comment, Screenshot, Challenge, User
from .forms import CommentForm, ErrorForm, RegisterUserForm, UserUpdateForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from bs4 import BeautifulSoup
import uuid
import boto3

S3_BASE_URL = 'https://s3-website.ca-central-1.amazonaws.com'
BUCKET = 'errordiary'


class ErrorCreate(LoginRequiredMixin, CreateView):
  model = Error

  form_class = ErrorForm
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ErrorUpdate(LoginRequiredMixin, UpdateView):
  model = Error
  form_class = ErrorForm

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
    new_comment.user_id = request.user.id
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

@login_required
def user_profile(request):
  message = ''
  if request.method == 'POST':
    user = User.objects.get(id=request.user.id)
    update_form = UserUpdateForm(request.POST, instance=user)
    if update_form.is_valid():
      update_form.save()
      message = f'Your profile has been updated!'
      return redirect('user_profile')

  else:
    user = User.objects.get(id=request.user.id)
    update_form = UserUpdateForm(instance=user)

  context = {
    'user': user,
    'update_form': update_form,
    'message': message
    }
  return render(request, 'user/detail.html', context)

def challenges_index(request):
  challenges = Challenge.objects.all()
  return render(request, 'challenges/index.html', { 'problems': challenges })

def challenge_detail(request, challenge_id):
  challenge = Challenge.objects.get(id=challenge_id)
  return render(request, 'challenges/detail.html', {'problem': challenge})

def scrape(request):
    data = requests.get('https://projecteuler.net/archives;page=10')
    soap = BeautifulSoup(data.content, 'html5lib')
    page_no = soap.find(class_='pagination noprint').find_all('a')[-1].text
    for page in range(1 , int(page_no)+1):
        page =  requests.get(f'https://projecteuler.net/archives;page={page}')
        soap = BeautifulSoup(page.content, 'html5lib')
        last_problem_no = soap.find_all(class_='id_column')[-1].text
        first_problem_number = soap.find_all(class_='id_column')[1].text
        for problem in range(int(first_problem_number),int(last_problem_no)+1):
            print(f'page number: {page} problem number: {problem}')
            problem_model = Challenge()
            problem_data = requests.get(f'https://projecteuler.net/problem={problem}')
            soap = BeautifulSoup(problem_data.content, 'html5lib')
            problem_model.title = soap.find_all('h2')[0].text
            problem_model.problem = soap.find_all('h3')[0].text
            problem_model.description = soap.find_all(class_='problem_content')[0].text
            problem_model.save()
        
    return redirect('/')

def add_screenshot(request, error_id):
  screenshot_file = request.FILES.get('screenshot-file', None)
  print(screenshot_file)
  if screenshot_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + screenshot_file.name[screenshot_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(screenshot_file, BUCKET, key)
      url = f"{S3_BASE_URL}/{BUCKET}/{key}"
      screenshot = Screenshot(url=url, error_id=error_id, user=request.user)
      screenshot.save()
    except:
      print('An Error occurred uploading file to S3')
  return redirect(f'/errors/{error_id}', error_id=error_id)