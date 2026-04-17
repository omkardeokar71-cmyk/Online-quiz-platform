from django.db import models

# Create your models here.
class Quiz(models.Model):
class Question(models.Model):
class Choice(models.Model):
class UserAttempt(models.Model):
Quiz → Question → Choice
       ↑
   UserAttempt