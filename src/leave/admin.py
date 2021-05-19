from django.contrib import admin
from leave.models import Leave

# Register your models here.
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('username', 'leavetype','startdate', 'enddate', 'relievername')
    list_filter = ('leavetype', 'status')
    readonly_fields = ('created', 'updated')
   
admin.site.register(Leave, LeaveAdmin)