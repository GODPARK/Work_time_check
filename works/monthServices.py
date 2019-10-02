from .models import WorkTimeCheck, BreakTimeCheck
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from pytz import timezone, utc
from django.conf import settings

class MonthServiceMethods:

    def __init__(self):
        self.KST = timezone('Asia/Seoul')

    def monthListDict(self, userId):
        nowDate = datetime.now(self.KST)
        serverDate = nowDate.strftime("%Y-%m-%d")
        
        try:
            todayBreak = BreakTimeCheck.objects.filter(personId=userId,todayDate=serverDate).all()

            totalTime = [0,0,0]
            tempTotalTime = [0,0,0]

            for tempData in todayBreak:
                tempList = tempData.totalBreakTime.split(':')
                tempTotalTime[2] += int(tempList[2])
                tempTotalTime[1] += int(tempList[1])
                tempTotalTime[0] += int(tempList[0])
            
            totalTime[2] = divmod(tempTotalTime[2] , 60 )[1]
            totalTime[0], totalTime[1] = divmod( divmod(tempTotalTime[2] , 60 )[0]  + tempTotalTime[1] , 60 )
            totalTime[0] += tempTotalTime[0]


            result = str(totalTime[0]) + ":" + str(totalTime[1]) + ":" + str(totalTime[2])
            

            returnData = {"result":"success", "personId":userId, "serverDate":serverDate, "currentTime":result, "method":"currentBreakTime"}
            return Response(returnData,status=status.HTTP_201_CREATED)

        except:
            returnData = {"result":"fail", "personId":userId, "serverDate":serverDate, "method":"currentBreakTime"}
            return Response(returnData,status=status.HTTP_400_BAD_REQUEST)
