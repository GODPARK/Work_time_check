from .models import WorkTimeCheck
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer


class ServiceMethods:
    
    def __init__(self):
        None

    def updateWorkStartTime(self,data,modifyDate):
        nowDate = datetime.now()
        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
        userId  = data['personId']

        if len(data) != 0:
            
            try: 
                if modifyDate != 'none':
                    todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate,workStatus=1)
                    todayWork.workStatus = 1
                    todayWork.workStartTime = serverTime
                    todayWork.save()
                    return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workStartPostApi"}, status=status.HTTP_201_CREATED)                
                
                elif modifyDate == 'none' and WorkTimeCheck.objects.filter(personId=userId,todayDate=serverDate).count() == 0:
                    data['todayDate'] = serverDate
                    data['workStartTime'] = serverTime
                    data['workEndTime'] = 'none'
                    data['totalWorkTime'] = 'none'
                    data['workStatus'] = 1
                    
                    serializer = WorkTimeCheckSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    
                    return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workStartPostApi"}, status=status.HTTP_201_CREATED)
                
                else:
                    return Response({ "result" : "fail" , "personId" : userId, "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)

            except:
                return Response({ "result" : "fail" , "personId" : userId, "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)



    def updateWorkEndTime(self,data):
        nowDate = datetime.now()
        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
        userId  = data['personId']

        if len(data) != 0:
            
            try: 
                todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate,workStatus=1)
                todayWork.workStatus = 1
                
                startTime = serverDate +" " + todayWork.workStartTime
                dateTypeTime = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
                totalTime = nowDate - dateTypeTime
                totalStringTime = str(totalTime).split('.')[0]

                todayWork.workEndTime = serverTime
                todayWork.totalWorkTime = totalStringTime

                todayWork.save()
                return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workEndPostApi"}, status=status.HTTP_201_CREATED)
            except:
                return Response({ "result" : "fail" , "personId" : userId, "method" : "workEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "workEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)