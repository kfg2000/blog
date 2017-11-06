from django.db import models

class Post(models.Model):
	title = models.CharField(max_length=225)
	content = models.TextField()
	updated = models.DateTimeField(auto_now = True)
	timestamp = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.title