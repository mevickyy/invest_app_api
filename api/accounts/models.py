from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    wallet = models.FloatField(blank=False)

class CreateProfile():
	def __init__(self, obj):
		self.user_data = obj

	def create(self):
		''' Update User Profile '''
		person, created = Profile.objects.update_or_create(
							  user_id=self.user_data.get('id'), defaults=dict(bio=self.user_data.get('bio'), wallet=settings.INITIAL_FUND)
							)
		return created