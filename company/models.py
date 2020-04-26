from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
	name = models.TextField(max_length=255)
	share_price = models.FloatField(blank=False)
	location = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)