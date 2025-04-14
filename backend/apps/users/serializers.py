from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if not attrs.get('email') and not attrs.get('phone_number'):
            raise serializers.ValidationError("Either email or phone number is required")
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            identifier=validated_data.get('email') or validated_data.get('phone_number'),
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number')
        )
        return user

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get('username')
        password = attrs.get('password')
        
        if not identifier or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'")
        
        # Authenticate via email or phone
        user = authenticate(
            request=self.context.get('request'),
            username=identifier,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        data = super().validate(attrs)
        refresh = self.get_token(user)
        
        data['user'] = UserSerializer(user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        return data

class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['phone_number'] = user.phone_number
        return token
