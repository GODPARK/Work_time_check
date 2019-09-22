from .models import WorkTimeCheck
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from pytz import timezone, utc
from django.conf import settings


class ServiceMethods:

    def __init__(self):
        self.KST = timezone('Asia/Seoul')

    def updateWorkStartTime(self, data, modifyDate):
        nowDate = datetime.now(self.KST)

        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
        userId  = data['personId']

        try: 
            if modifyDate != 'none':
                todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate,workStatus=1)
                todayWork.workStatus = 1
                todayWork.workStartTime = serverTime
                todayWork.save()

                return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workStartPostApi"}, status=status.HTTP_201_CREATED)                
                
            elif modifyDate == 'none' and WorkTimeCheck.objects.filter(personId=userId,todayDate=serverDate).count() == 0:
                    
                saveData = {}
                saveData['personId'] = userId
                saveData['todayDate'] = serverDate
                saveData['workStartTime'] = serverTime
                saveData['workEndTime'] = 'none'
                saveData['totalWorkTime'] = 'none'
                saveData['workStatus'] = 1
                    
 
                serializer = WorkTimeCheckSerializer(data=saveData)
                if serializer.is_valid():
                    serializer.save()
                    
                return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workStartPostApi"}, status=status.HTTP_201_CREATED)
                
            else:
                return Response({ "result" : "fail" , "personId" : userId, "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({ "result" : "fail" , "personId" : userId, "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)



    def updateWorkEndTime(self,data):
        nowDate = datetime.now(self.KST)
        nowDateString = nowDate.strftime("%Y-%m-%d %H:%M:%S").split('.')[0]
        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
        userId  = data['personId']
            
        try: 
            todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate,workStatus=1)
            todayWork.workStatus = 1

            startTime = serverDate + " " + todayWork.workStartTime
            dateTypeTime = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
            nowTypeTime = datetime.strptime(nowDateString,'%Y-%m-%d %H:%M:%S')
            totalTime = nowTypeTime - dateTypeTime
            
            totalStringTime = str(totalTime).split('.')[0]
            todayWork.workEndTime = serverTime
            todayWork.totalWorkTime = totalStringTime
            todayWork.save()

            return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workEndPostApi"}, status=status.HTTP_201_CREATED)
        except:
            return Response({ "result" : "fail" , "personId" : userId, "method" : "workEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "workEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)
