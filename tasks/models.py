from django.db import models

class Task(models.Model):
	PRIORITY_CHOICES = [
		("low", "Low"),
		("medium", "Medium"),
		("high", "High"),
	]

	title = models.CharField(max_length=200)
	body = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	due_date = models.DateField(null=True, blank=True)
	completed = models.BooleanField(default=False)
	completed_at = models.DateTimeField(null=True, blank=True)
	priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")

	def __str__(self):
		return self.title
# Create your models here.
