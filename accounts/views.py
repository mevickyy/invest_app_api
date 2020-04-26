from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer
from accounts.models import CreateProfile


class UserRegistrationAPIView(CreateAPIView):
	''' User Registration '''
	authentication_classes = ()
	permission_classes = ()
	serializer_class = UserRegistrationSerializer

	def create(self, request, *args, **kwargs):
		''' CREATE USER '''
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)

		user = serializer.instance
		token, created = Token.objects.get_or_create(user=user) #Generate the token key once user registration
		data = serializer.data
		data["token"] = token.key
		data["bio"] = request.data.get('bio')
		CreateProfile(data).create() #Trigger the account profile for update wallet
		headers = self.get_success_headers(serializer.data)
		return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
	''' User Login API '''
	authentication_classes = ()
	permission_classes = ()
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		''' Once User do login will return the token key '''
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			user = serializer.user
			token, _ = Token.objects.get_or_create(user=user) #Generated Token and stored into auth token models
			return Response(
				data=TokenSerializer(token).data,
				status=status.HTTP_200_OK,
			)
		else:
			return Response(
				data=serializer.errors,
				status=status.HTTP_400_BAD_REQUEST,
			)


class UserTokenAPIView(RetrieveDestroyAPIView):
	''' UserToken API View for retrieve and logout the session '''
	lookup_field = "key"
	serializer_class = TokenSerializer
	queryset = Token.objects.all()

	def filter_queryset(self, queryset):
		return queryset.filter(user=self.request.user)

	def retrieve(self, request, key, *args, **kwargs):
		''' Retrieve the user from token based '''
		if key == "current":
			instance = Token.objects.get(key=request.auth.key) # Here Auth key is get from header Authorization
			serializer = self.get_serializer(instance)
			return Response(serializer.data)
		return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

	def destroy(self, request, key, *args, **kwargs):
		''' Delete the token for logout the JWT token ''' 
		if key == "current":
			Token.objects.get(key=request.auth.key).delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)