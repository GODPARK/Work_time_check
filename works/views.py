from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from .models import WorkTimeCheck, BreakTimeCheck, CurrentStatus
from datetime import datetime

# Create your views here.
def index(request):
    todayWork = WorkTimeCheck.objects.get(personId="hyun937",todayDate="2019-09-21")
    context = { 'today' : todayWork }    
    return render(request,'works/index.html' , context)

@api_view(['POST'])
def workStartPostApi(request):
    
    nowDate = datetime.now()
    serverDate = nowDate.strftime("%Y-%m-%d")
    serverTime = nowDate.strftime("%H:%M:%S")

    if len(request.data) != 0:
        todayWork = WorkTimeCheck.objects.get(personId=request.data['personId'],todayDate=serverDate,workStatus=0)
        todayWork.workStatus = 0
        todayWork.workStartTime = serverTime
        todayWork.save()

        return Response(request.data, status=status.HTTP_201_CREATED)
    
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def workInfoGetApi(request):
    serializer = WorkTimeCheckSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
