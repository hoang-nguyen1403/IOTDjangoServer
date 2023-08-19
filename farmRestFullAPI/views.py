import json

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from . import gate_way as gw
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def control_fan(request):
    if request.method == 'POST':
        action = json.loads(request.body)['action']
        gate_wave_obj.fan_action(action)
    return HttpResponse(status=204)


@csrf_exempt
def control_pump(request):
    if request.method == 'POST':
        action = json.loads(request.body)['action']
        gate_wave_obj.pump_action(action)
    return HttpResponse(status=204)


@csrf_exempt
def control_led(request):
    if request.method == 'POST':
        action = json.loads(request.body)['action']
        gate_wave_obj.led_action(action)
    return HttpResponse(status=204)
