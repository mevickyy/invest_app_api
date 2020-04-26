from django.contrib.auth.models import User
from company.models import Company
from accounts.models import Profile
from investment.models import Investments
from rest_framework import serializers


class InvestmentSerializer(serializers.ModelSerializer):
	''' Investment Serializer to validate for CREATE, UPDATE, DELETE '''
	company_id = serializers.IntegerField()
	invested_amount = serializers.FloatField()

	class Meta:
		model = Investments
		fields = ("id", "company_id", "invested_amount")

	def validate(self, attrs):
		''' validate if invested amount should be greater than 0 and not lessthan or equalto 0 '''
		if attrs.get('invested_amount') < 0 or not attrs.get('invested_amount') > 0:
			raise serializers.ValidationError({"invested_amount":"Amount should be greater than 0"})
		return attrs

class InvestmentViewSerializer(serializers.ModelSerializer):
	''' Investment View Serializer to RETRIEVE the all investments lists '''
	class Meta:
		model = Investments
		fields = ("id", "company_id", "user_share", "invested_amount")