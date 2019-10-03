from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer , SuggestionsSerializer
from .models import WorkTimeCheck, BreakTimeCheck, CurrentStatus ,Suggestion
from datetime import datetime
from .services import ServiceMethods
from .modifyServices import ModifyServiceMethods
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json

#SERVERIP = "http://192.168.0.4:8000"
SERVERIP = "http://34.84.171.132"
#SERVERIP = "http://127.0.0.1:8000"
SERVERAPIIP = SERVERIP + "/works/api/"

# Create your views here.
''' 
    html rendering 하는 부분
'''

@login_required
def index(request):
    if 'personId' in request.COOKIES:
        return render(request,'works/index.html', { 'personId' : request.COOKIES['personId'], 'serverApiIp' : SERVERAPIIP, 'serverIp' : SERVERIP})
    else:
        return render(request,'works/login.html')


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

@login_required
def month(request):
    if 'personId' in request.COOKIES:
        data = { 'personId' : request.COOKIES['personId'], 'serverApiIp' : SERVERAPIIP, 'serverIp' : SERVERIP }
        return render(request,'works/month.html', data )
    else:
        return render(request,'works/login.html')

@login_required
def modifyWork(request):
    if 'personId' in request.COOKIES:
        data = { 'personId' : request.COOKIES['personId'], 'serverApiIp' : SERVERAPIIP, 'serverIp' : SERVERIP }
        return render(request,'works/modify.html', data )
    else:
        return render(request,'works/login.html')

@login_required
def notice(request):
    if 'personId' in request.COOKIES:
        suggestion = Suggestion.objects.all()
        data = { 
            'personId' : request.COOKIES['personId'], 
            'serverApiIp' : SERVERAPIIP, 
            'serverIp' : SERVERIP,
            'updateDate' : "2019-10-03",
            'updateList' : "공지사항 기능 추가, 제안 기능 추가, 출/퇴근 시간 수정 가능",
            'todoList' : '한달 업무 시간 확인 , 휴게 시간 수정 기능',
            'suggestion' : suggestion
            }
        
        return render(request,'works/notice.html', data )
    else:
        return render(request,'works/login.html')

'''
    service.py api call
    업무 시간 및 휴식 시간 체크 API  
'''
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


'''
    modifyService.py api call
    업무 시간 및 휴식 시간 수동 수정용 API  
'''
@api_view(['POST'])
def modifyWorkSearchApi(request):
    modifyService = ModifyServiceMethods()
    return modifyService.modifySearchWork(request.COOKIES['personId'],request.data)

@api_view(['POST'])
def modifyWorkApi(request):
    modifyService = ModifyServiceMethods()
    return modifyService.modifyWork(request.COOKIES['personId'],request.data)


'''
    notice api call
'''
@api_view(['POST'])
def suggestionApi (request):
    
    try:
        saveData = {}
        print(request.data)
        saveData['personId'] = request.COOKIES['personId']
        saveData['content'] = request.data['suggestion']
        
        serializer = SuggestionsSerializer(data=saveData)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({ "result" : "fail", "method" : "suggestionApi"}, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response({ "result" : "fail", "method" : "suggestionApi"}, status=status.HTTP_400_BAD_REQUEST)

    returnData = {}
    return Response(returnData,status=status.HTTP_201_CREATED)
