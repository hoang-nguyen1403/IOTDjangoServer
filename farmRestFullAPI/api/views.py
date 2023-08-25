from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework import viewsets

from rest_framework.authentication import BasicAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework import generics
from farmRestFullAPI.models import Employee, User, ControlPanel, Profile, RoomCondition, Automation, AutomationStatus
from farmRestFullAPI.api.serializers import \
    EmployeeSerializer, UserSerializer, ControlPanelSerializer, \
    ProfileSerializer, RoomConditionSerializer, AutomationSerializer, AutomationStatusSerializer


class ControlPanelViewSet(viewsets.ModelViewSet):
    queryset = ControlPanel.objects.all()
    serializer_class = ControlPanelSerializer

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def addaction(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'added': True})
    @action(detail=True,
            methods=['get'],
            serializer_class=ControlPanelSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @action(detail=True,
            methods=['get'],
            serializer_class=UserSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    @action(detail=True,
            methods=['get'],
            serializer_class=ProfileSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def uploadProfile(self, request, *args, **kwargs):
        print("========", request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'added': True})


class RoomConditionViewSet(viewsets.ModelViewSet):
    queryset = RoomCondition.objects.all()
    serializer_class = RoomConditionSerializer

    @action(detail=True,
            methods=['get'],
            serializer_class=RoomConditionSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AutomationViewSet(viewsets.ModelViewSet):
    queryset = Automation.objects.all()
    serializer_class = AutomationSerializer

    @action(detail=True,
            methods=['get'],
            serializer_class=AutomationSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AutomationStatusViewSet(viewsets.ModelViewSet):
    queryset = AutomationStatus.objects.all()
    serializer_class = AutomationStatusSerializer

    @action(detail=True,
            methods=['get'],
            serializer_class=AutomationStatusSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)