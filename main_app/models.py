from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

LANGUAGES = (
  ('JS', 'Javascript'),
  ('HTML', 'HTML'),
  ('CSS', 'CSS'),
  ('PY', 'Python'),
  ('NJS', 'Node.js')
)


class Error(models.Model):
  title = models.CharField(max_length=100)
  language = models.CharField(
    max_length=10,
    choices=LANGUAGES,
    default=LANGUAGES[0][0]
  )
  description = models.TextField()
  solution = models.TextField()
  date = models.DateField('error date')
  user = models.ForeignKey(User, on_delete=models.CASCADE)

 
  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('error_detail', kwargs={'error_id' : self.id })   

class Comment(models.Model):
  error = models.ForeignKey(Error, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text_input = models.TextField()
  date = models.DateField('comment date')

  def __str__(self):
    return self.text_input 
    
class Screenshot(models.Model):
  url = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  error = models.ForeignKey(Error, on_delete=models.CASCADE)

class Problem(models.Model):
  title = models.CharField(max_length=1000)
  problem = models.CharField(max_length=1000)
  description = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

class UserAvatar(models.Model):
  avatar = models.ImageField(upload_to=None)
  user = models.OneToOneField(User)

  def set_avatar(self):
       self.has_picture = True


# class Upvote(models.Model):
#   error = models.ForeignKey(Error, on_delete=models.CASCADE)
#   # user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Downvote(models.Model):
#   error = models.ForeignKey(Error, on_delete=models.CASCADE)
#   # user = models.ForeignKey(User, on_delete=models.CASCADE)






