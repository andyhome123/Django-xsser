from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class record(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    data = models.TextField(blank=True, null=True)
    paramter = models.TextField(blank=True, null=True)

class project(models.Model):
    id = models.CharField(max_length=36, primary_key=True, unique=True)
    title = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    get_paramter = models.TextField(blank=True,null=True)
    js = models.BooleanField(default=False)
    js_content = models.TextField(blank=True,null=True)
    records = models.ManyToManyField(record, blank=True)


class account(models.Model):
    user_id = models.OneToOneField(User)
    project = models.ManyToManyField(project, blank=True)



