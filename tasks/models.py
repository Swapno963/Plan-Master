from django.db import models

# Create your models here.
from projects.models import Project
from django.contrib.auth.models import User
# for constrains
from .constants import PRIORITYS, CURRENT_STATUS

class Tasks(models.Model):
    user = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    due_date = models.DateField()
    priority = models.CharField(max_length = 100,choices = PRIORITYS) 
    current_status = models.CharField(max_length = 100,choices = CURRENT_STATUS) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
  

    def __str__(self):
      return f"{self.title}-{self.project}"
  