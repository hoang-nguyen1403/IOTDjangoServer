from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework import viewsets

from rest_framework.authentication import BasicAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework import generics
from farmRestFullAPI.models import Employee, User, ControlPanel
from farmRestFullAPI.api.serializers import \
    EmployeeSerializer, UserSerializer, ControlPanelSerializer


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
        user = serializer.save()
        return Response({'added': True})

    @action(detail=True,
            methods=['get'],
            serializer_class=ControlPanelSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# class ControlPanelListView(generics. ListAPIView):
#   queryset = ControlPanel.objects.all()
#     serializer_class = ControlPanelSerializer
#
#
#
# class ControlPanelDetailView(generics.RetrieveAPIView):
#     queryset = ControlPanel.objects.all()
#     serializer_class = ControlPanelSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # @action(detail=True,
    #         methods=['post'],
    #         authentication_classes=[BasicAuthentication],
    #         permission_classes=[IsAuthenticated])
    # def addaction(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     return Response({'added': True})

    @action(detail=True,
            methods=['get'],
            serializer_class=EmployeeSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class UserListView(generics. ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


