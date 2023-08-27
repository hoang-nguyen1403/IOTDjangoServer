import json
from datetime import datetime

from django.http import JsonResponse
from bokeh.plotting import figure, show
from bokeh.embed import components
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, RoomCondition, Automation, AutomationStatus, ControlPanel
from django.core.paginator import Paginator
from django.utils import timezone
import pytz
from . import gate_way as gw

# Create your views here.
# gate_wave_obj = None
gate_wave_obj = gw.go()
PANEL_CONTROL_URL = 'http://127.0.0.1:8000/api/panelcontrol/'
AUTOMATION_CONTROL_URL = 'http://127.0.0.1:8000/api/automation/'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def dashboard(request):
    all_posts_auto = list(Automation.objects.order_by('created'))
    all_posts_auto_status = list(AutomationStatus.objects.order_by('created'))
    all_devices_status = list(ControlPanel.objects.order_by('created'))

    if len(all_posts_auto) == 0:
        return
    latest_data_auto = all_posts_auto[-1]
    latest_data_auto_status = all_posts_auto_status[-1]
    latest_devices_status = all_devices_status[-1]
    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard', 'latest_data_auto': latest_data_auto,
                   'latest_status': latest_data_auto_status,
                   'latest_devices_status': latest_devices_status} )


class NotificationProcessor():
    def __init__(self, all_actions):
        self.all_actions = all_actions

    def get_notification_list(self):
        notification_list = []
        for idx, action in enumerate(self.all_actions):
            if idx == len(self.all_actions) - 1:
                break
            username = action.author.username
            created = action.created

            utc_timezone = pytz.timezone('UTC')
            bangkok_timezone = pytz.timezone('Asia/Bangkok')
            timestamp_utc = created.astimezone(utc_timezone)
            # Convert the UTC timestamp to Bangkok time
            local_start_time = timestamp_utc.astimezone(bangkok_timezone)
            # Format the converted timestamp as a string
            local_start_time_str = local_start_time.strftime("%Y-%m-%d %H:%M:%S")
            hasFan = action.hasFan
            hasPump = action.hasPump
            hasLed = action.hasLed

            notification = {
                "username": username,
                "created": local_start_time_str
            }
            message = ""

            previus_fan_status = self.all_actions[idx + 1].hasFan
            previus_led_status = self.all_actions[idx + 1].hasLed
            previus_pump_status = self.all_actions[idx + 1].hasPump

            fan_status = "on" if previus_fan_status else "off"
            led_status = "on" if previus_led_status else "off"
            pump_status = "on" if previus_pump_status else "off"

            if previus_fan_status != hasFan:
                message +=  f"Fan was turn {fan_status},"

            if previus_led_status != hasLed:
                message +=  f" Led was turn {led_status},"

            if previus_pump_status != hasPump:
                message +=  f" Pump was turn {pump_status}."

            if message != "":
                notification["message"] = message

                notification_list.append(notification)
        notification_list.reverse()
        return notification_list


@login_required
def home(request):
    all_posts = list(RoomCondition.objects.order_by('created'))
    if len(all_posts) == 0:
        return
    latest_data = all_posts[-1]

    all_actions = list(ControlPanel.objects.order_by('created'))
    notification_processor = NotificationProcessor(all_actions)

    notification_list = notification_processor.get_notification_list()
    # print(notification_list)

    paginator = Paginator(notification_list, 3)
    page_number = request.GET.get('page', 1)
    rendering_notification_list = paginator.page(page_number)

    return render(request, 'account/home.html', {
        'section': 'home',
        "latest_data": latest_data,
        "notifications": rendering_notification_list
    } )


@login_required
def chart(request):
    #create a plot
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # create a new plot with a title and axis labels
    p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness to the plot
    p.line(x, y, legend_label="Temp.", line_width=2)
    script,div = components(p)
    context = {
        'script':script,
        'div':div,
        'section': 'chart'
    }

    return render(request, 'account/chart.html', context )


@csrf_exempt
def control_device(request):
    if request.method == 'POST':
        status = 200
        data = json.loads(request.body)
        state = data['state']
        device_name = data['device_name']
        if state:
            action = 'ON'
        else:
            action = 'OFF'
        if device_name == "led":
            gate_wave_obj.led_action(action)
            response_message = f"Turn {action} Led"
        elif device_name == "fan":
            gate_wave_obj.fan_action(action)
            response_message = f"Turn {action} Fan"
        elif device_name == "pump":
            gate_wave_obj.pump_action(action)
            response_message = f"Turn {action} Pump"
        else:
            response_message = f"Couldn't find any device with name {device_name}"
            status = 400
        return HttpResponse(response_message, status=status)
    return HttpResponse('Invalid request method', status=405)


def check_room_status(request):
    status_object = RoomCondition.objects.first()  # Get the first status object
    json_data = {}
    json_data['temperature'] = status_object.temperature
    json_data['soilmoisture'] = status_object.soilmoisture
    json_data['light_intensity'] = status_object.light_intensity
    if status_object:
        return JsonResponse(json_data)
    else:
        return JsonResponse({"status": False})


def update_room_data(request):
    all_posts = list(RoomCondition.objects.order_by('created'))
    if len(all_posts) == 0:
        return
    latest_data = all_posts[-1]
    json_data = {}
    json_data['temperature'] = latest_data.temperature
    json_data['soilmoisture'] = latest_data.soilmoisture
    json_data['light_intensity'] = latest_data.light_intensity
    if latest_data:
        return JsonResponse({"latest_data": json_data})
    else:
        return JsonResponse({"status": False})
