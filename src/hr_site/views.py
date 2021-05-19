from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from leave.models import Leave
from employees.models import *


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method =='POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username or Password is incorrect')
				
		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url=('login'))
def index_view(request):
	user = request.user
	
	dataset = dict()
	all_employees = Employee.objects.all()
	all_leaves = Leave.objects.all()
	employees_birthday = Employee.objects.birthdays_current_month()
	staff_leaves = Leave.objects.filter(username = user)
		
	
	dataset['all_employees'] = all_employees
	dataset['all_leaves'] = all_leaves
	dataset['employees_birthday'] = employees_birthday
	dataset['staff_leaves'] = staff_leaves
	dataset['dashboard_page'] = "active"	
		
	return render(request,'index.html', dataset)
