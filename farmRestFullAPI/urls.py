from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # previous login view
    path('control_device/', views.control_device, name='control'),
    path('check_room_status/', views.check_room_status, name='room_status'),
    path('update_room_data/', views.update_room_data, name='room_data'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password urls
    # path('password-change/',
    #      auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password-change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(),
    #      name='password_change_done'),
    #
    # # change password urls
    # path('password-change/',
    #      auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password-change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(),
    #      name='password_change_done'),
    #
    # # reset password urls
    # path('password-reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password-reset/complete/',
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),

    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('', views.home, name='home'),
]