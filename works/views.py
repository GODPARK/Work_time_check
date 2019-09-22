from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from .models import WorkTimeCheck, BreakTimeCheck, CurrentStatus
from datetime import datetime
from .services import ServiceMethods
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'works/index.html')

@api_view(['POST'])
def workStartPostApi(request):
    service = ServiceMethods()
    return service.updateWorkStartTime(request.data, 'none')


@api_view(['POST'])
def workEndPostApi(request):
    service = ServiceMethods()
    return service.updateWorkEndTime(request.data)

