from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Employee, Department, Position

class DateInput(forms.DateInput):
    input_type= 'date'


class CreateUserForm(UserCreationForm):    
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmployeeCreateForm(ModelForm): 
    image = forms.ImageField(widget=forms.FileInput())     
    class Meta:
        model = Employee
        exclude = ['is_blocked','is_deleted','created','createdby','updated']
        widgets = {'dateofbirth': DateInput(), 'employmentdate': DateInput(), 'terminationdate': DateInput() }


class DepartmentForm(ModelForm):
    
    class Meta:
        model = Department
        fields = ["name","description"]

class PositionForm(ModelForm):
    
    class Meta:
        model = Position
        fields = ["department","name","description"]
