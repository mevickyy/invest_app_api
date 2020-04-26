from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from company.models import Company
from django.conf import settings


class CompanySerializer(serializers.ModelSerializer):
	''' Company Serializer to validate for CREATE, UPDATE, DELETE '''
	name = serializers.CharField(
			required=True,
			validators=[UniqueValidator(queryset=Company.objects.all())]
			)
	share_price = serializers.FloatField()
	location = serializers.CharField(min_length=2)

	class Meta:
		model = Company
		fields = ("id", "name", "share_price", "location")

	def validate(self, attrs):
		''' Maximum share price is not morethan 699 also notlessthan 0'''
		if attrs.get('share_price') > settings.SHARE_PRICE or attrs.get('share_price') < 1:
			raise serializers.ValidationError({"share_price":"Share Price value should be lessthan than {} and greaterthan 0".format(settings.SHARE_PRICE)})
		return attrs