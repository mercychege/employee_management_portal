from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
from .models import Employee, Department, Position
from leave.models import Leave
from .forms import EmployeeCreateForm, CreateUserForm, DepartmentForm, PositionForm


# Create your views here.
def createUser(request):  
    if not request.user.is_authenticated:
        return redirect('/')
    
    submitted = False
    if request.method == 'POST':        
        form = CreateUserForm(request.POST,request.FILES)
        if form.is_valid():                    
            form.save()          
            return HttpResponseRedirect('/employees/createuser?submitted=True')
        else:
           messages.info(request, 'Please fill in all the required fields') 
    else:
        form = CreateUserForm()
        if 'submitted' in request.GET:
            submitted = True
 
    return render(request, 'employees/create_user.html',{'form': form, 'submitted': submitted, 'createuser_page': "active"})


class EmployeeList(ListView):
    model = Employee    
    context_object_name='all_employees'

    def get_context_data(self, **kwargs):      
        context = super(ListView, self).get_context_data(**kwargs)
              
        all_leaves = Leave.objects.all()
        active_employees = Employee.objects.all_active_employees()
        inactive_employees = Employee.objects.all_blocked_employees() 
        employees_birthday = Employee.objects.birthdays_current_month()
               
   
        context['all_leaves'] = all_leaves
        context['active_employees'] = active_employees
        context['inactive_employees'] = inactive_employees
        context['employees_birthday'] = employees_birthday
        context['employees_page'] = "active"         
                
        return context


class EmployeeView(DetailView):
    model = Employee
    context_object_name = 'employee'
 
    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        context['employees_page'] = "active" 
        return context
        
def employee_create(request):
    if not request.user.is_authenticated:
        return redirect('/')
   
    submitted = False
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST,request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            try:
                employee.createdby = request.user
            except Exception:
                pass
            employee.save()          
            return HttpResponseRedirect('/employees/add?submitted=True')
        else:
           messages.info(request, 'Please fill in all the required fields') 
    else:
        form = EmployeeCreateForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'employees/employee_create.html', {'form': form, 'submitted': submitted, 'employees_page': "active"})


def profile_view(request):
    user = request.user
    if user.is_authenticated:
        employee = Employee.objects.filter(username = user).first()
        dataset = dict()
        dataset['employee'] = employee
        dataset['userprofile_page'] = "active"
        return render(request,'employees/employee_profile.html',dataset)    
    return redirect('/')



def employee_edit(request,id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
   
    employee = get_object_or_404(Employee, id = id)
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST or None,request.FILES or None,instance = employee)
        if form.is_valid():
            instance = form.save(commit=False)
            
            user = request.POST.get('username')
            assigned_user = User.objects.get(id = user)

            instance.employeenumber = request.POST.get('employeenumber')
            instance.username = assigned_user			
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.gender = request.POST.get('gender')         
            instance.dateofbirth = request.POST.get('dateofbirth')
            instance.maritalstatus = request.POST.get('maritalstatus')

            instance.address = request.POST.get('address')
            instance.postcode = request.POST.get('postcode')
            instance.lastname = request.POST.get('lastname')
            instance.phone = request.POST.get('phone')
            instance.email = request.POST.get('email')       

            department = request.POST.get('department')
            department_instance = Department.objects.get(id = department)
            instance.department = department_instance

            position = request.POST.get('position')
            position_instance = Position.objects.get(id = position)
            instance.position = position_instance

            instance.ID_No = request.POST.get('ID_No')
            instance.Passport_No = request.POST.get('Passport_No')
            instance.NSSF_No = request.POST.get('NSSF_No')
            instance.NHIF_No = request.POST.get('NHIF_No')
            instance.KRA_No = request.POST.get('KRA_No')
            instance.employmentdate = request.POST.get('employmentdate')
            instance.employmenttype = request.POST.get('employmenttype')
            instance.terminationdate = request.POST.get('terminationdate')

            instance.bankname = request.POST.get('bankname')
            instance.bankbranch = request.POST.get('bankbranch')
            instance.bankaccount = request.POST.get('bankaccount')

            instance.save()
            messages.success(request,'Account Updated Successfully !!!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('employee:detail-employees', pk = id)

        else:

            messages.error(request,'Error Updating account',extra_tags = 'alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    dataset = dict()
    form = EmployeeCreateForm(request.POST or None,request.FILES or None,instance = employee)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(employee.get_full_name)
    dataset['employees_page'] = "active"
    return render(request,'employees/employee_create.html',dataset)


def birthday_month(request):	
    user = request.user
    if not request.user.is_authenticated:
        return redirect('/')

    employees = Employee.objects.birthdays_current_month()
    month = datetime.date.today().strftime('%B')
    all_leaves = Leave.objects.all()
    all_employees = Employee.objects.all()
    staff_leaves = Leave.objects.filter(username = user)
	
    
    context = {    
    'employees_birthday': employees,
    'month':month,
    'count_birthdays':employees.count(),    
    'all_leaves': all_leaves,
    'all_employees': all_employees,
    'staff_leaves':staff_leaves,
    'birthday_page':"active"
    
	}
    return render(request,'employees/employee_birthdays.html',context)


class DepartmentList(ListView):
    model = Department    
    context_object_name='all_departments'

    def get_context_data(self, **kwargs):      
        context = super(ListView, self).get_context_data(**kwargs)
              
        all_positions = Position.objects.all()
        context['all_positions'] = all_positions
        context['departments_page'] = "active"
           
        return context
    

def createDeparment(request):
    if not request.user.is_authenticated:
        return redirect('/')
    submitted = False
    if request.method == 'POST':
        form = DepartmentForm(request.POST,request.FILES)
        if form.is_valid():                    
            form.save()          
            return HttpResponseRedirect('/employees/departments/add?submitted=True')
        else:
           messages.info(request, 'Please fill in all the required fields') 
    else:
        form = DepartmentForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'employees/create_department.html', {'form': form, 'submitted': submitted, 'departments_page':"active"})


class PositionList(ListView):
    model = Position    
    context_object_name='all_positions'

    def get_context_data(self, **kwargs):      
        context = super(ListView, self).get_context_data(**kwargs)
              
        all_departments = Department.objects.all()
        context['all_departments'] = all_departments
        context['positions_page'] = "active" 
           
        return context


def createPosition(request):
    if not request.user.is_authenticated:
        return redirect('/')
    submitted = False
    if request.method == 'POST':
        form = PositionForm(request.POST,request.FILES)
        if form.is_valid():                    
            form.save()          
            return HttpResponseRedirect('/employees/positions/add?submitted=True')
        else:
           messages.info(request, 'Please fill in all the required fields') 
    else:
        form = PositionForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'employees/create_position.html', {'form': form, 'submitted': submitted, 'positions_page': "active"})