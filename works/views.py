from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from .models import WorkTimeCheck, BreakTimeCheck, CurrentStatus
from datetime import datetime
from .services import ServiceMethods
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def index(request):
    # SERVERIP = "192.168.0.4"
    return render(request,'works/index.html', { 'personId' : request.COOKIES['personId']})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/works/')
        else:
            return render(request,'works/login.html',{"error" : "user info is incorrect"})
    return render(request,'works/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')

@api_view(['POST'])
def workStartPostApi(request):
    service = ServiceMethods()
    return service.updateWorkStartTime(request.COOKIES['personId'],  'none')

@api_view(['POST'])
def workEndPostApi(request):
    service = ServiceMethods()
    return service.updateWorkEndTime(request.COOKIES['personId'])

@api_view(['POST'])
def currentWorkTimeApi(request):
    service = ServiceMethods()
    return service.currentWorkTime(request.COOKIES['personId'])

@api_view(['POST'])
def breakStartPostApi(request):
    service = ServiceMethods()
    return service.updateBreakStartTime(request.COOKIES['personId'])

@api_view(['POST'])
def breakEndPostApi(request):
    service = ServiceMethods()
    return service.updateBreakEndTime(request.COOKIES['personId'])

@api_view(['POST'])
def currentBreakApi(request):
    service = ServiceMethods()
    return service.currentBreakTime(request.COOKIES['personId'])

@api_view(['POST'])
def dayOffApi(request):
    service = ServiceMethods()
    return service.dayOff(request.COOKIES['personId'])
    
@api_view(['POST'])
def totalWorkApi(request):
    service = ServiceMethods()
    return service.finalWorkTime(request.COOKIES['personId'])