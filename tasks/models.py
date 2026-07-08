from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
	STATUS_CHOICES = [
		("notStarted", "Not Started"),
		("inProgress", "In Progress"),
		("completed", "Completed"),
	]
	PRIORITY_CHOICES = [
		("low", "Low"),
		("medium", "Medium"),
		("high", "High")
	]
	CATEGORY_CHOICES = [
		("work", "Work"),
		("dog", "Dog Stuff"),
		("gym", "Gym"),
		("housework", "Housework"),
		("shopping", "Shopping"),
		("miscellaneous", "Miscellaneous")
	]
	title = models.CharField(max_length=200)
	body = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	due_date = models.DateField(null=True, blank=True)
	completed_at = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="notStarted")
	priority = models.CharField(max_length=200, choices=PRIORITY_CHOICES, default="low")
	category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default="miscellaneous")
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
# Create your models here.
