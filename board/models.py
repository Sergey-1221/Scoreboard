from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=150)

	def __str__(self):
		return self.name

class Task(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name + " | " + self.category.name

class Success_task(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)