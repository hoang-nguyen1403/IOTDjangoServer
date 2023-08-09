from django.urls import path, include
# from rest_framework import routers
from . import views
from rest_framework import routers

app_name = 'farmRestFullAPI'

router = routers.DefaultRouter()
router.register('panelcontrol', views.ControlPanelViewSet)
router.register('user', views.UserViewSet)
router.register('profile', views.ProfileViewSet)
router.register('roomcondition', views.RoomConditionViewSet)




urlpatterns = [

    # path('/add', views.ControlPanelViewSet, name='control_devices'),

    # path('controlPanelApi/',
    #      views.ControlPanelListView.as_view(),
    #      name='controlPanelApi_list'),

    # path('users/',
    #      views.UserListView.as_view(),
    #      name='user_list'),
    # path('employee/<UserDetailView>/',
    #      views.EmployeeDetailView.as_view(),
    #      name='user_detail'),
    #
    # path('employee/',
    #      views.EmployeeListView.as_view(),
    #      name='employee_list'),
    # path('employee/<pk>/',
    #      views.EmployeeDetailView.as_view(),
    #      name='employee_list_detail'),
    path('', include(router.urls)),

]
