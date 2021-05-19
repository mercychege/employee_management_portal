from django.urls import path
from . import views
from .views import EmployeeList, EmployeeView, DepartmentList, PositionList

app_name = 'employee'

urlpatterns = [
	path('createuser/', views.createUser, name='create-user'),
	path('all/', EmployeeList.as_view(), name='all-employees'),	
	path('view/<int:pk>', EmployeeView.as_view(), name='detail-employees'),
	path('add/', views.employee_create, name= 'add-employees'),
	path('edit/<int:id>/',views.employee_edit,name='edit-employees'),
	path('profile', views.profile_view, name='user-profile'),
	path('departments/', DepartmentList.as_view(), name= 'all-departments'),
	path('departments/add/', views.createDeparment, name= 'add-departments'),
	path('positions/', PositionList.as_view(), name= 'all-positions'),
	path('positions/add/', views.createPosition, name= 'add-positions'),
	path('birthdays', views.birthday_month, name='employee-birthdays'),
    
]

