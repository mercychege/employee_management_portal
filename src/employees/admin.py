from django.contrib import admin
from employees.models import Employee, Position, Department

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeenumber','firstname', 'lastname', 'email', 'position',)
    list_filter = ('employeenumber', 'firstname', 'is_blocked',)
    readonly_fields = ('created', 'createdby','updated')
    fieldsets = (
        ('Personal Information', {
            'classes': ('collapse',),
            'fields': ('employeenumber', 'username', 'image','firstname', 'lastname', 'othername', 'gender', 'dateofbirth', 'maritalstatus')
        }),
        ('Contact Information', {
            'classes': ('collapse',), 
            'fields': ('address', 'postcode', 'currentresidence', 'phone', 'email')
        }),
        ('Employment Information', {
            'classes': ('collapse',), 
            'fields': ('department', 'position', 'ID_No', 'Passport_No', 'NSSF_No', 'NHIF_No', 'KRA_No', 'employmentdate', 'employmenttype', 'terminationdate')
        }), 
        ('Bank Account Information', {
            'classes': ('collapse',),
            'fields': ('bankname', 'bankbranch', 'bankaccount')
        }),

         ('Additional Information', {
            'classes': ('collapse',),
            'fields': ('is_blocked', 'is_deleted', 'created','createdby', 'updated')
        }),
    )



# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Position)