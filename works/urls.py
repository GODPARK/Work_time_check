from django.urls import path
from . import views

app_name= 'works'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/start',views.workStartPostApi, name="startTime" ),
    path('api/end', views.workEndPostApi, name = "EndTime"),
    path('api/currentTime', views.currentWorkTimeApi, name="CurrentTime"),
    path('api/break/start', views.breakStartPostApi, name="breakStartTime"),
    path('api/break/end', views.breakEndPostApi, name="breakEndTime"),
    path('api/break/total', views.currentBreakApi, name="CurrentBreak"),
    path('api/dayoff', views.dayOffApi, name="dayOff"),
    path('api/total', views.totalWorkApi, name="totalTime")

]