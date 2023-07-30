from rest_framework import serializers
from farmRestFullAPI.models import Employee, ControlPanel
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'author', 'slug']

class ControlPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlPanel
        fields = ['id', 'author',
                  'created', 'hasFan', 'hasPump','hasLed']


