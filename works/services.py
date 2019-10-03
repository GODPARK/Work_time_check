from .models import WorkTimeCheck, BreakTimeCheck
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkTimeCheckSerializer, BreakTimeCheckSerializer, CurrentStatusSerializers, WorkStartTimeSaveSerializer
from pytz import timezone, utc
from django.conf import settings


class ServiceMethods:

    def __init__(self):
        self.KST = timezone('Asia/Seoul')

    def currentWorkTime(self,userId):
        nowDate = datetime.now(self.KST)
        nowDateString = nowDate.strftime("%Y-%m-%d %H:%M:%S").split('.')[0]
        serverDate = nowDate.strftime("%Y-%m-%d")
        
        try:
            todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate)

            if todayWork.workStatus == 1:
                
                startTime = serverDate + " " + todayWork.workStartTime
                dateTypeTime = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
                nowTypeTime = datetime.strptime(nowDateString,'%Y-%m-%d %H:%M:%S')
                totalTime = nowTypeTime - dateTypeTime

                totalStringTime = str(totalTime).split('.')[0]
                workPercent = str(int((int(totalStringTime.split(":")[0]) /8 )*100)) + "%"

                returnData = {"result":"success", "personId":userId, "serverDate":serverDate, "currentTime":totalStringTime, "workPercent" : workPercent, "method":"currentWorkTime"}
                return Response(returnData,status=status.HTTP_201_CREATED)

            elif todayWork.workStatus == 2:
                workPercent = str(int((int(todayWork.totalWorkTime.split(":")[0]) /8 )*100)) + "%"
                returnData = {"result":"success", "personId":userId, "serverDate":serverDate, "currentTime":todayWork.totalWorkTime, "workPercent" : workPercent, "method":"currentWorkTime"}
                return Response(returnData,status=status.HTTP_201_CREATED)
            elif todayWork.workStatus == 99:
                returnData = {"result":"success", "personId":userId, "serverDate":serverDate, "currentTime":"DAY OFF", "method":"currentWorkTime"}
                return Response(returnData,status=status.HTTP_201_CREATED)
            else:
                returnData = {"result":"fail", "personId":userId, "serverDate":serverDate, "method":"currentWorkTime"}
                return Response(returnData,status=status.HTTP_400_BAD_REQUEST)
        except:
            returnData = {"result":"fail", "personId":userId, "serverDate":serverDate, "method":"currentWorkTime"}
            return Response(returnData,status=status.HTTP_400_BAD_REQUEST)



    def updateWorkStartTime(self,userId, modifyDate):
        nowDate = datetime.now(self.KST)

        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
        
        try: 
            if modifyDate != 'none':
                todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate,workStatus=1)
                todayWork.workStatus = 1
                todayWork.workStartTime = serverTime
                todayWork.dayNum = nowDate.day
                todayWork.monthNum = nowDate.month
                todayWork.yearNum = nowDate.year
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
                saveData['dayNum'] = nowDate.day
                saveData['monthNum'] = nowDate.month
                saveData['yearNum'] = nowDate.year
                    
 
                serializer = WorkTimeCheckSerializer(data=saveData)
                if serializer.is_valid():
                    serializer.save()
                    
                return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workStartPostApi"}, status=status.HTTP_201_CREATED)
                
            else:
                return Response({ "result" : "fail" , "personId" : userId, "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({ "result" : "fail" , "personId" : userId, "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "workStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)



    def updateWorkEndTime(self,userId):
        nowDate = datetime.now(self.KST)
        nowDateString = nowDate.strftime("%Y-%m-%d %H:%M:%S").split('.')[0]
        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
            
        try: 
            todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate,workStatus__in=[1,2])
            todayWork.workStatus = 2

            startTime = serverDate + " " + todayWork.workStartTime
            dateTypeTime = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
            nowTypeTime = datetime.strptime(nowDateString,'%Y-%m-%d %H:%M:%S')
            totalTime = nowTypeTime - dateTypeTime
            
            #점심 시간 포함 
            # totalStringTime = str(totalTime + timedelta(hours=-1)).split('.')[0]
            # 점심 시간 미포함
            totalStringTime = str(totalTime).split('.')[0]

            todayWork.workEndTime = serverTime
            todayWork.totalWorkTime = totalStringTime
            todayWork.save()

            return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "workEndPostApi"}, status=status.HTTP_201_CREATED)
        except:
            return Response({ "result" : "fail" , "personId" : userId, "method" : "workEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "workEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)


    def updateBreakStartTime(self,userId):
        nowDate = datetime.now(self.KST)
        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
        
        try: 
            if BreakTimeCheck.objects.filter(personId=userId,todayDate=serverDate,breakStatus=1).count() == 0:   
                saveData = {}
                saveData['personId'] = userId
                saveData['todayDate'] = serverDate
                saveData['breakStartTime'] = serverTime
                saveData['breakEndTime'] = 'none'
                saveData['totalBreakTime'] = 'none'
                saveData['breakStatus'] = 1
                    
 
                serializer = BreakTimeCheckSerializer(data=saveData)
                if serializer.is_valid():
                    serializer.save()
                        
                return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "serverTime" : serverTime, "method" : "breakStartPostApi"}, status=status.HTTP_201_CREATED)
            else:
                return Response({ "result" : "fail" , "personId" : userId, "method" : "breakStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        except:
            return Response({ "result" : "fail" , "personId" : userId, "method" : "breakStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "breakStartPostApi"}, status=status.HTTP_400_BAD_REQUEST)


    def updateBreakEndTime(self,userId):
        nowDate = datetime.now(self.KST)
        nowDateString = nowDate.strftime("%Y-%m-%d %H:%M:%S").split('.')[0]
        serverDate = nowDate.strftime("%Y-%m-%d")
        serverTime = nowDate.strftime("%H:%M:%S")
            
        try: 
            todayBreak = BreakTimeCheck.objects.get(personId=userId,todayDate=serverDate,breakStatus=1)
            todayBreak.breakStatus = 2

            startTime = serverDate + " " + todayBreak.breakStartTime
            dateTypeTime = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
            nowTypeTime = datetime.strptime(nowDateString,'%Y-%m-%d %H:%M:%S')
            totalTime = nowTypeTime - dateTypeTime
            
            totalStringTime = str(totalTime).split('.')[0]
            todayBreak.breakEndTime = serverTime
            todayBreak.totalBreakTime = totalStringTime
            todayBreak.save()

            return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "currentTime":todayBreak.totalBreakTime, "serverTime" : serverTime, "method" : "breakEndPostApi"}, status=status.HTTP_201_CREATED)
        except:
            return Response({ "result" : "fail" , "personId" : userId, "method" : "breakEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "breakEndPostApi"}, status=status.HTTP_400_BAD_REQUEST)



    def currentBreakTime(self,userId):
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


    def dayOff(self,userId):
        nowDate = datetime.now(self.KST)
        serverDate = nowDate.strftime("%Y-%m-%d")
        
        try:
            if WorkTimeCheck.objects.filter(personId=userId,workStatus=99).count()==0 :
                saveData = {}
                saveData['personId'] = userId
                saveData['todayDate'] = serverDate
                saveData['workStartTime'] = 'none'
                saveData['workEndTime'] = 'none'
                saveData['totalWorkTime'] = 'dayOff'
                saveData['workStatus'] = 99
                        
    
                serializer = WorkTimeCheckSerializer(data=saveData)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"result" : "success", "personId" : userId, "serverDate" : serverDate, "method" : "dayOff"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({ "result" : "fail" , "personId" : userId, "method" : "dayOff"}, status=status.HTTP_400_BAD_REQUEST)
                            
            else:
                return Response({ "result" : "fail" , "personId" : userId, "method" : "dayOff"}, status=status.HTTP_400_BAD_REQUEST)            

        except:
            return Response({ "result" : "fail" , "personId" : userId, "method" : "dayOff"}, status=status.HTTP_400_BAD_REQUEST)            

        return Response({ "result" : "fail" , "personId" : userId , "method" : "dayOff"}, status=status.HTTP_400_BAD_REQUEST)


    def finalWorkTime(self,userId):
        nowDate = datetime.now(self.KST)
        serverDate = nowDate.strftime("%Y-%m-%d")
        
        try:
            todayWork = WorkTimeCheck.objects.get(personId=userId,todayDate=serverDate,workStatus=2)
            
            todayTotal = todayWork.totalWorkTime
            
            print(todayTotal)

            totalTime = [0,0,0]
            tempTotalTime = [0,0,0]
            tempWorkTime = todayTotal.split(":")
            tempTotalTime[2] += int(tempWorkTime[2])
            tempTotalTime[1] += int(tempWorkTime[1])
            tempTotalTime[0] += int(tempWorkTime[0])

            todayBreak = BreakTimeCheck.objects.filter(personId=userId,todayDate=serverDate).all()


            for tempData in todayBreak:
                tempList = tempData.totalBreakTime.split(':')
                tempTotalTime[2] -= int(tempList[2])
                tempTotalTime[1] -= int(tempList[1])
                tempTotalTime[0] -= int(tempList[0])

            print(tempTotalTime)

            totalTime[2] = divmod(tempTotalTime[2] , 60 )[1]
            totalTime[0], totalTime[1] = divmod( divmod(tempTotalTime[2] , 60 )[0]  + tempTotalTime[1] , 60 )
            totalTime[0] += tempTotalTime[0]


            result = str(totalTime[0]-1) + "시간 " + str(totalTime[1]) + "분 " + str(totalTime[2]) + "초"

            returnData = {"result":"success", "personId":userId, "serverDate":serverDate, "currentTime":result, "method":"finalWorkTime"}
            return Response(returnData,status=status.HTTP_201_CREATED)
            
        except:
            returnData = {"result":"fail", "personId":userId, "serverDate":serverDate, "method":"finalWorkTime"}
            return Response(returnData,status=status.HTTP_400_BAD_REQUEST)