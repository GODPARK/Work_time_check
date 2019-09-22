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
import json

# Create your views here.
def index(request):
    return render(request,'works/index.html')

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
    return service.updateWorkStartTime(json.loads(request.data), 'none')

@api_view(['POST'])
def workEndPostApi(request):
    service = ServiceMethods()
    return service.updateWorkEndTime(json.loads(request.data))

@api_view(['POST'])
def currentWorkTimeApi(request):
    
    service = ServiceMethods()
    return service.currentWorkTime(json.loads(request.data))