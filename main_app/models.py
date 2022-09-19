from django.db import models
from datetime import date
# from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

langauges = (
  ('JS', 'Javascript'),
  ('HTML', 'HTML'),
  ('CSS', 'CSS'),
  ('PY', 'Python'),
  ('NJS', 'Node.js')
)


class Error(models.Model):
  title = models.CharField(max_length=100)
  language = models.CharField(max_length=50)
  description = models.TextField()
  solution = models.TextField()
  date = models.DateField('error date')
  # user = models.ForeignKey(User, on_delete=models.CASCADE)

 
  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('error_detail', kwargs={'error_id' : self.id })   

class Comment(models.Model):
   error = models.ForeignKey(Error, on_delete=models.CASCADE)
   text_input = models.TextField()
   date = models.DateField('comment date')

   def __str__(self):
    return self.text_input 
    
class Screenshot(models.Model):
  url = models.CharField(max_length=200)
  # user = models.ForeignKey(User, on_delete=models.CASCADE)
  error = models.ForeignKey(Error, on_delete=models.CASCADE)





