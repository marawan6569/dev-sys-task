from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Status


class UserSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', 'iso-8601'])

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'country_code',
                  'gender', 'birthdate']


class CreateUserSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', 'iso-8601'])

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name', 'country_code',
                  'gender', 'birthdate', 'avatar', 'email', 'password']


class AuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must include "phone_number" and "password"'
            raise Exception(msg)

        attrs['user'] = user
        return attrs


class CreateStatusSerializer(serializers.Serializer):

    def create(self, validated_data):
        user = User.objects.get(phone_number=validated_data['phone_number'])
        status = Status(user=user, status=validated_data['status'])
        status.save()
        return status

    _status_choices = (
        ('inactive', 'inactive'),
        ('active', 'active'),
        ('superuser', 'superuser'),
    )
    token = serializers.CharField()
    status = serializers.ChoiceField(choices=_status_choices)
    phone_number = serializers.CharField()

    class Meta:
        fields = ['phone_number', 'status', 'token']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
