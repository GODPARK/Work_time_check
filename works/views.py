from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from .models import WorkTimeCheck, BreakTimeCheck, CurrentStatus
from datetime import datetime
from .services import ServiceMethods

# Create your views here.
def index(request):
    todayWork = WorkTimeCheck.objects.get(personId=request.data['personId'],todayDate="2019-09-22")
    context = { 'today' : todayWork }    
    return render(request,'works/index.html' , context)

@api_view(['POST'])
def workStartPostApi(request):
    service = ServiceMethods()
    return service.updateWorkStartTime(request.data, 'none')


@api_view(['POST'])
def workEndPostApi(request):
    service = ServiceMethods()
    return service.updateWorkEndTime(request.data)


@api_view(['GET'])
def workInfoGetApi(request):
    serializer = WorkTimeCheckSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
