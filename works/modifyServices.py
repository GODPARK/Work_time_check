from .models import WorkTimeCheck, BreakTimeCheck
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from pytz import timezone, utc
from django.conf import settings

class ModifyServiceMethods:
    def __init__(self):
        self.KST = timezone('Asia/Seoul')
    
    def modifyWork(self,userId,date):
        print(date['searchDate'])
        returnData = {"result":"success", "personId":userId, "serverDate":date['searchDate'], "method":"currentBreakTime"}
        return Response(returnData,status=status.HTTP_201_CREATED)