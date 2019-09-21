from rest_framework import serializers
from .models import WorkTimeCheck, BreakTimeCheck, CurrentStatus

class WorkTimeCheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkTimeCheck
        fields = (
            'personId',
            'workStartTime',
            'workEndTime',
            'todayDate',
            'totalWorkTime',
            'workStatus'
             )

class WorkStartTimeSaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkTimeCheck
        fields = (
            'personId',
            'workStartTime',
            'todayDate'
             )

class BreakTimeCheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BreakTimeCheck
        fields = (
            'personId',
            'todayDate',
            'breakStartTime',
            'breakEndTime',
            'totalBreakTime',
            'breakStatus',
        )

class CurrentStatusSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrentStatus
        fields = (
            'personId',
            'currentState'
        )