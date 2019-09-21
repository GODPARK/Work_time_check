from django.urls import path
from . import views

app_name= 'works'
urlpatterns = [
    path('', views.index, name='index'),
    path('info/get', views.workInfoGetApi, name="info"),
    path('api/start',views.workStartPostApi, name="startTime" )
]