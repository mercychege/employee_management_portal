from django.db import models
from django.contrib.auth.models import User
from .manager import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
import datetime
# Create your models here.
GENDER = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('NOT_KNOWN', 'Not Known')
)

MARITAL_STATUS = (
    ('MARRIED','Married'),
    ('SINGLE','Single'),
    ('DIVORCED','Divorced'),
    ('WIDOW','Widow'),
    ('WIDOWER','Widower')
)

EMPLOYEMENTTYPE = (
    ('FULL_TIME','Full-Time'),
    ('PART_TIME','Part-Time'),
    ('CONTRACT','Contract'),
    ('INTERN','Intern'),
    )

class Department(models.Model):
    
    name = models.CharField(max_length=125, blank=False)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        
    
    def __str__(self):
        return self.name

class Position(models.Model):
    '''
        Role Table eg. Staff,Manager,H.R ...
    '''
    department = models.ForeignKey(Department(), blank=False, null=True, on_delete=models.SET_NULL) 
    name = models.CharField(max_length=125, blank=False)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
       


    def __str__(self):
        return self.name


class Employee(models.Model):
    # Personal Information
    employeenumber = models.CharField(max_length=30,null=True,blank=True) 
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)   
    image = models.FileField(('Profile Image'),upload_to='profiles/',default='profiles/default.png',blank=True, null=True, help_text='upload image size less than 2.0MB')
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=100, null=False, blank=False)
    othername = models.CharField(('Othername (optional)'),max_length=100,null=True,blank=True)
    gender = models.CharField(max_length=9, choices=GENDER,blank=False)
    dateofbirth = models.DateField(default='YYYY-MM-DD',blank=False, null=False)
    maritalstatus = models.CharField(max_length=9, choices=MARITAL_STATUS,blank=False)
    
    # Contact Information    
    address = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=200, blank=True)
    currentresidence = models.CharField(max_length=200, blank=True)
    phone = PhoneNumberField(default='+254 700000000',max_length=15, blank=True)
    email = models.EmailField()  

    # Employment Information
    department =  models.ForeignKey(Department,verbose_name =_('Department'),on_delete=models.SET_NULL,null=True,default=None)
    position =  models.ForeignKey(Position,verbose_name =_('Position'),on_delete=models.SET_NULL,null=True,default=None)
    ID_No = models.CharField(max_length=200, blank=True)
    Passport_No = models.CharField(max_length=200, blank=True)
    NSSF_No = models.CharField(max_length=200, blank=True)
    NHIF_No = models.CharField(max_length=200, blank=True)
    KRA_No = models.CharField(max_length=200, blank=True)
    employmentdate = models.CharField(max_length=200, blank=True)
    employmenttype = models.CharField(max_length=50, choices=EMPLOYEMENTTYPE,blank=False)
    terminationdate = models.CharField(max_length=200, blank=True)
    # Bank Account Information
    bankname = models.CharField(_('Name of Bank'),max_length=125,blank=False,null=True,help_text='')
    bankbranch = models.CharField(_('Branch'),help_text='Which branch was the account issue',max_length=125,blank=True,null=True)
    bankaccount = models.CharField(_('Account Number'),help_text='employee account number',max_length=30,blank=False,null=True)
    
    # Leave Details
     
    # Additional Information
    is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is Deleted'),help_text='button to toggle employee deleted and undelete',default=False)
 
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True) 
    createdby = models.ForeignKey(User, blank=True, null=True, related_name="creator",on_delete=models.SET_NULL)   
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)

    objects = EmployeeManager()

    def __str__(self):
        return str(self.employeenumber)

    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname +' '+ lastname
            return fullname
        elif othername:
            fullname = firstname + ' '+ lastname +' '+othername
            return fullname
        return

    @property
    def get_pretty_birthday(self):
        if self.dateofbirth:
            return self.dateofbirth.strftime('%A,%d %B') 
        return



    @property
    def birthday_today(self):       
        return self.dateofbirth.day == datetime.date.today().day



    @property
    def days_check_date_fade(self):
        '''
        Check if Birthday has already been celebrated ie in the Past     ie. 4th May  & today 8th May 4 < 8 -> past else present or future '''
        return self.dateofbirth.day < datetime.date.today().day #Assumption made,If that day is less than today day,in the past




    def birthday_counter(self):
        '''
        This method counts days to birthday -> 2 day's or 1 day
        '''
        today = datetime.date.today()
        current_year = today.year

        birthday = self.dateofbirth # eg. 5th May 1995

        future_date_of_birth = datetime.date(current_year,birthday.month,birthday.day)#assuming born THIS YEAR ie. 5th May 2019

        if birthday:
            if (future_date_of_birth - today).days > 1:

                return str((future_date_of_birth - today).days) + ' day\'s'

            else:

                return ' tomorrow'

        return
