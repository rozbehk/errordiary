from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Screenshot(models.Model):
  url = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)


class Error(models.Model):
  title = models.CharField(max_length=100)
  language = models.CharField(max_length=50)
  description = models.TextField()
  screenshot = models.ForeignKey(Screenshot, on_delete=models.CASCADE)
  date = models.DateField('comment date')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
 

  def __str__(self):
    return self.title

class Comment(models.Model):
   error = models.ForeignKey(Error, on_delete=models.CASCADE)
   text_input = models.TextField()
   screenshot = models.ForeignKey(Screenshot, on_delete=models.CASCADE)
   date = models.DateField('solution date')

   def __str__(self):
    return self.text_input

class Error(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
