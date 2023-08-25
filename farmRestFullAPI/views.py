import json
from bokeh.plotting import figure, show
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, RoomCondition
from . import gate_way as gw

# Create your views here.
gate_wave_obj = None
# gate_wave_obj = gw.go()


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
    return render(request, 'account/dashboard.html', {'section': 'dashboard'} )

@login_required
def home(request):
    all_posts = list(RoomCondition.objects.order_by('created'))
    if len(all_posts) == 0:
        return
    latest_data = all_posts[-1]
    return render(request, 'account/home.html', {'section': 'home', "latest_data": latest_data } )



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
    
    return render(request, 'account/chart.html', {'section': 'chart'} )



@csrf_exempt
def control_fan(request):
    if request.method == 'POST':
        action = json.loads(request.body)['action']
        gate_wave_obj.fan_action(action)
    return HttpResponse(status=204)


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
