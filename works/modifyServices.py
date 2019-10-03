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

    def dateCheck(self, date):

        if date == "":
            return False

        dateList = str(date).split(":")
        
        if len(dateList) != 3:
            return False
        
        try:
            int(dateList[0])
            int(dateList[1])
            int(dateList[2])
        except:
            return False
        
        if 0 > int(dateList[0]) or 24 < int(dateList[0]):
            return False
        if 0 > int(dateList[1]) or 59 < int(dateList[1]):
            return False
        if 0 > int(dateList[2]) or 59 < int(dateList[2]):
            return False
        
        return True
    
    def modifySearchWork(self,userId,date):
        
        returnData = {}
        try:
            todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=str(date['searchDate']),workStatus__in=[1,2])
        
            if todayWork.workStatus == 1:
                
                returnData = {
                    "result":"success", 
                    "personId":userId, 
                    "serverDate":str(date['searchDate']), 
                    "beforeStartWork" : todayWork.workStartTime,
                    "beforeEndWork": '아직 퇴근 이전입니다.',
                    "beforeTotalWork" : '아직 퇴근 이전입니다.',
                    "method":"modifySearchWork"
                }

            elif todayWork.workStatus == 2:
                
                returnData = {
                    "result":"success", 
                    "personId":userId, 
                    "serverDate":date['searchDate'], 
                    "beforeStartWork" : todayWork.workStartTime,
                    "beforeEndWork": todayWork.workEndTime,
                    "beforeTotalWork" : todayWork.totalWorkTime,
                    "method":"modifySearchWork"
                }

            else:
                return Response({ "result" : "fail" , "personId" : userId , "method" : "modifySearchWork"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(returnData,status=status.HTTP_201_CREATED)

        except:
            return Response({ "result" : "fail" , "personId" : userId , "method" : "modifySearchWork"}, status=status.HTTP_400_BAD_REQUEST)




    def modifyWork(self,userId,date):

        returnData = {}
        
        dateWork = str(date['searchDate'])
        
        try:
            todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=dateWork,workStatus__in=[1,2])
        
            if todayWork.workStatus == 1 :
                
                if self.dateCheck(date['modifyWorkStartTime']):
                    todayWork.workStartTime = date['modifyWorkStartTime']
                    todayWork.save() 
            
                returnData = {
                    "result":"success", 
                    "personId":userId, 
                    "serverDate":date['searchDate'], 
                    "afterTotalWork" : '아직 퇴근 이전입니다.',
                    "method":"modifyWork"
                    }
                
            elif todayWork.workStatus == 2 :
                
                if not self.dateCheck(date['modifyWorkStartTime']) and not self.dateCheck(date['modifyWorkEndTime']):
                    return Response({ "result" : "fail" , "personId" : userId , "method" : "modifyWork"}, status=status.HTTP_400_BAD_REQUEST)

                if self.dateCheck(date['modifyWorkStartTime']):
                    todayWork.workStartTime = date['modifyWorkStartTime']
                    startTime = dateWork + " " + date['modifyWorkStartTime']
                    endTime = dateWork + " " + todayWork.workEndTime
                    dateTypeStart = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
                    dateTypeEnd = datetime.strptime(endTime,'%Y-%m-%d %H:%M:%S')
                    totalTime = dateTypeEnd - dateTypeStart
            
                    totalStringTime = str(totalTime).split('.')[0]
                    todayWork.totalWorkTime = totalStringTime
                    returnData = {
                        "result":"success", 
                        "personId":userId, 
                        "serverDate":date['searchDate'], 
                        "afterTotalWork" : totalStringTime,
                        "method":"modifyWork"
                        }
                                        
                if self.dateCheck(date['modifyWorkEndTime']):
                    todayWork.workEndTime = date['modifyWorkEndTime']
                    startTime = dateWork + " " + todayWork.workStartTime
                    endTime = dateWork + " " + date['modifyWorkEndTime']
                    dateTypeStart = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
                    dateTypeEnd = datetime.strptime(endTime,'%Y-%m-%d %H:%M:%S')
                    totalTime = dateTypeEnd - dateTypeStart
            
                    totalStringTime = str(totalTime).split('.')[0]
                    todayWork.totalWorkTime = totalStringTime
                    returnData = {
                        "result":"success", 
                        "personId":userId, 
                        "serverDate":date['searchDate'], 
                        "afterTotalWork" : totalStringTime,
                        "method":"modifyWork"
                        }

                if self.dateCheck(date['modifyWorkStartTime']) and self.dateCheck(date['modifyWorkEndTime']):
                    
                    startTime = dateWork + " " + date['modifyWorkStartTime']
                    endTime = dateWork + " " + date['modifyWorkEndTime']
                    dateTypeStart = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
                    dateTypeEnd = datetime.strptime(endTime,'%Y-%m-%d %H:%M:%S')
                    totalTime = dateTypeEnd - dateTypeStart
            
                    totalStringTime = str(totalTime).split('.')[0]
                    todayWork.totalWorkTime = totalStringTime
                    returnData = {
                        "result":"success", 
                        "personId":userId, 
                        "serverDate":date['searchDate'], 
                        "afterTotalWork" : totalStringTime,
                        "method":"modifyWork"
                        }
                

                todayWork.save()

            else:
                return Response({ "result" : "fail" , "personId" : userId , "method" : "modifyWork"}, status=status.HTTP_400_BAD_REQUEST)


            return Response(returnData,status=status.HTTP_201_CREATED)
            
        except:
            return Response({ "result" : "fail" , "personId" : userId , "method" : "modifyWork"}, status=status.HTTP_400_BAD_REQUEST)
        


