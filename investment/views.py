from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from investment.serializers import InvestmentSerializer, InvestmentViewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from company.models import Company
from investment.models import Investments
from accounts.views import UserTokenAPIView
from rest_framework import serializers
from accounts.models import Profile
from django.conf import settings

class CreateInvestmentAPIView(CreateAPIView):
	''' Create Investments API is based on user_id and company_id to create investments  '''
	queryset = Investments.objects.all()
	permission_classes = [IsAuthenticated]
	serializer_class = InvestmentSerializer

	def create(self, request, *args, **kwargs):
		''' Create function for investments '''
		serializer = self.get_serializer(data=request.data)	
		serializer.is_valid(raise_exception=True)
		user_id = Token.objects.get(key=request.auth.key).user_id #GET user_id from TOKEN model

		invested_amount = serializer.validated_data['invested_amount']
		company_id = serializer.validated_data['company_id']
		total_amount = Profile.objects.get(user_id=user_id).wallet #Fetch wallet info amount from profile table
		balance_amount = Utility().is_fund(invested_amount, total_amount) #Deduction Amount after investment	
		serializer.validated_data['user_id'] = user_id
		serializer.validated_data['user_share'] = Utility().share_price(company_id, invested_amount) #number of shares of company invested

		self.perform_create(serializer) #Save the record
		Utility().update_wallet(user_id, balance_amount) #once inserted update the wallet balance			
		data = serializer.validated_data
		headers = self.get_success_headers(serializer.data) #pass header authorization
		return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class Utility:
	''' Utility Function for Create and Update Investment API to check fund and sharprice calculation '''
	def is_fund(self, invested_amount, total_amount):
		if invested_amount > total_amount:
			raise serializers.ValidationError({"error": "Insufficient Fund. You don't have enought funds to invest", "account_balance":total_amount})		
		return (total_amount - invested_amount) #Deduct investamount from user main balance

	def share_price(self, company_id, invested_amount):
		''' Number of shares of company invested'''
		share_price = Company.objects.get(id=company_id).share_price
		return invested_amount / share_price #The calculation will work according investing_amount / company_shareprice

	def update_wallet(self, user_id, balance_amount):
		''' Update balance_amount of after deduction using this API Function'''
		Profile.objects.update_or_create(
			user_id=user_id,
			defaults={'wallet': balance_amount},
		)


class InvestmentListAPIView(ListAPIView):
	''' List out user investment list along with total investment amount '''
	queryset = Investments.objects
	serializer_class = InvestmentViewSerializer
	permission_classes = [IsAuthenticated]

	def list(self, request):
		''' Investment List API Function'''
		user_id = Token.objects.get(key=request.auth.key).user_id
		queryset = self.get_queryset().filter(user_id=user_id)		
		serializer = InvestmentViewSerializer(queryset, read_only=True, many=True)
		serializer_data = serializer.data # get the default serialized data 
		total_amount = Profile.objects.get(user_id=user_id).wallet #Fetch wallet info amount from profile table
		serializer_data.append({"total_invested_amount": settings.INITIAL_FUND - total_amount}) #Append total investment amount dict who spend against all companies
		return Response(serializer_data) 


class UpdateInvestmentAPIView(UpdateAPIView):
	''' Update Investment API is for if user wants to change the invest amount or else '''
	queryset = Investments.objects.all()
	serializer_class = InvestmentSerializer
	permission_classes = [IsAuthenticated]

	def update(self, request, *args, **kwargs):
		''' Update using instance serializer lookup field '''
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data)        
		serializer.is_valid(raise_exception=True) #Valid Serializer or not

		user_id = Token.objects.get(key=request.auth.key).user_id # Fetch user_id from TOKEN auth model
		company_id = instance.company_id
		wallet_amount = Profile.objects.get(user_id=user_id).wallet
		total_amount = (wallet_amount + instance.invested_amount) #while updating merge current invest amount + balance amount for deduct from this invested amount
		invested_amount = float(request.data.get('invested_amount'))	

		balance_amount = Utility().is_fund(invested_amount, total_amount)		
		serializer.validated_data['user_id'] = user_id
		serializer.validated_data['user_share'] = Utility().share_price(company_id, invested_amount) #number of shares of company invested

		self.perform_update(serializer) #Update force insert
		Utility().update_wallet(user_id, balance_amount) #once inserted update the wallet balance				
		return Response(serializer.data)

class DestroyInvestmentAPIView(DestroyAPIView):
	''' Destroy Investment API for delete their investment '''
	queryset = Investments.objects.all()
	serializer_class = InvestmentSerializer
	permission_classes = [IsAuthenticated]

	def destroy(self, request, *args, **kwargs):
		''' Delete the record from investment table '''
		instance = self.get_object()
		user_id = Token.objects.get(key=request.auth.key).user_id
		wallet_amount = Profile.objects.get(user_id=user_id).wallet
		balance_amount = wallet_amount + instance.invested_amount
		Utility().update_wallet(user_id, balance_amount) #once deleted add the deleted amount to the wallet	
		self.perform_destroy(instance) #perform delete
		return Response(status=status.HTTP_204_NO_CONTENT)
		return super(DestroyCompanyAPIView, self).destroy(request, key, *args, **kwargs)