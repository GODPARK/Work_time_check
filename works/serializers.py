from rest_framework import serializers
from .models import WorkTimeCheck, BreakTimeCheck, CurrentStatus, Suggestion

class WorkTimeCheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkTimeCheck
        fields = (
            'personId',
            'workStartTime',
            'workEndTime',
            'todayDate',
            'totalWorkTime',
            'workStatus',
            'dayNum',
            'monthNum',
            'yearNum'
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
            'dayNum',
            'monthNum',
            'yearNum'
        )

class SuggestionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Suggestion
        fields = (
            'personId',
            'content'
        )

class CurrentStatusSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrentStatus
        fields = (
            'personId',
            'currentState'
        )