from django.db import models

# Create your models here.
class WorkTimeCheck(models.Model):
    objects = models.Manager()
    personId = models.CharField(max_length=200)
    todayDate = models.CharField(max_length=200)
    yearNum =models.IntegerField(default=0)
    monthNum = models.IntegerField(default=0)
    dayNum = models.IntegerField(default=0)
    workStartTime = models.CharField(max_length=200)
    workEndTime = models.CharField(max_length=200)
    totalWorkTime  = models.CharField(max_length=300)
    workStatus = models.IntegerField(default=0)

   
class BreakTimeCheck(models.Model):
    objects = models.Manager()
    personId = models.CharField(max_length=200)
    todayDate = models.CharField(max_length=200)
    breakStartTime = models.CharField(max_length=200)
    breakEndTime = models.CharField(max_length=200)
    totalBreakTime = models.CharField(max_length=300)
    breakStatus = models.IntegerField(default=0)

   
class CurrentStatus(models.Model):
    objects = models.Manager()
    personId = models.CharField(max_length=200)
    currentState = models.CharField(max_length=300)

