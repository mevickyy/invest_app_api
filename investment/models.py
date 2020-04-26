from django.db import models
from django.contrib.auth.models import User
from company.models import Company
	
class Investments(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	invested_amount = models.FloatField(blank=False)
	user_share = models.FloatField(blank=False)
	date_modified = models.DateTimeField(auto_now=True)