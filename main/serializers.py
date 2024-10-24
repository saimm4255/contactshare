# serializers.py
from rest_framework import serializers
from .models import CustomUser, Profile, Contact

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'timezone', 'picture', 'is_active']

    def update(self, instance, validated_data):
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'name', 'phone_number', 'email', 'address', 'is_active']

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def validate_email(self, value):
        # Example of field-level validation
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must be an @example.com address.")
        return value

    def validate(self, data):
        # Object-level validation example
        if data['name'] == 'Invalid Contact':
            raise serializers.ValidationError("Contact name cannot be 'Invalid Contact'.")
        return data
