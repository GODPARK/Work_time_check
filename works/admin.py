from django.contrib import admin
from works.models import WorkTimeCheck, BreakTimeCheck, CurrentStatus

# Register your models here.
admin.site.register(WorkTimeCheck)
admin.site.register(BreakTimeCheck)
admin.site.register(CurrentStatus)