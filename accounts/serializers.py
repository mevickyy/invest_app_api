from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    ''' User Registration serailizer CREATE, UPDATE, DELETE'''
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    first_name = serializers.CharField(max_length=30, allow_blank=False)
    last_name = serializers.CharField(max_length=30, allow_blank=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password", "first_name", "last_name", "date_joined")

    def validate(self, attrs):
        ''' validate password and confirm password is matching or not '''
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password":"Those passwords don't match."})
        del attrs['confirm_password']
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserLoginSerializer(serializers.Serializer):
    ''' User Login Serializer for account status '''
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': 'User account is disabled.',
        'invalid_credentials': 'Unable to login with provided credentials.'
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        ''' validate the user for account is invalid or not '''
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active: #check user status
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    ''' Return the Auth Token '''
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")