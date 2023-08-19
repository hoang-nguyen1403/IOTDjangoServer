from rest_framework import serializers
from farmRestFullAPI.models import Employee, ControlPanel, Profile, RoomCondition
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            # Ensure password is write-only
        }

    def create(self, validated_data):
        # Hash the password before creating the user
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user',
                  "date_of_birth", "photo", "about_you"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'author', 'slug']


class ControlPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlPanel
        fields = ['id', 'author',
                  'created', 'hasFan', 'hasPump', 'hasLed']

class RoomConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCondition
        fields = ['id', 'created', 'temperature', 'soilmoisture' ]