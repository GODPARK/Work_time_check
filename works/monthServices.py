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
        tempMonth = int(nowDate.month)
        tempYear = int(nowDate.year)
        startList = [0 for _ in range(24)]
        endList = [0 for _ in range(24)]
        totalTimeList = [0,0,0]
        totalTime = [0,0,0]

        try:
            monthWork = WorkTimeCheck.objects.filter(personId=userId,yearNum=tempYear,monthNum=tempMonth,workStatus__in=[1,2]).all()
            
            for work in monthWork:
                startList[int(work.workStartTime.split(":")[0])] += 1

                if work.workEndTime != "none":
                    endList[int(work.workEndTime.split(":")[0])] += 1
                
                if work.totalWorkTime != "none":
                    tempTotalTime = work.totalWorkTime.split(":")
                    totalTimeList[0] += int(tempTotalTime[0])
                    totalTimeList[1] += int(tempTotalTime[1])
                    totalTimeList[2] += int(tempTotalTime[2])
                
            totalTime[2] = divmod(totalTimeList[2] , 60 )[1]
            totalTime[0], totalTime[1] = divmod( divmod(totalTimeList[2] , 60 )[0]  + totalTimeList[1] , 60 )
            totalTime[0] += totalTimeList[0]


            return { "monthWork" : monthWork, "startList" : startList, "endList" : endList, "totalTime" : str(totalTime[0])+":"+str(totalTime[1])+":"+str(totalTime[2])}

        except:
            return { "monthWork" : [], "startDict" : {}, "endDict" : {}, "totalTime" : "00:00:00"}
