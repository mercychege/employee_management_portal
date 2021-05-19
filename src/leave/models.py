from django.db import models
from .manager import LeaveManager
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
# Create your models here.
LEAVE_TYPE = (
('Sick','Sick Leave'),
('Casual','Casual Leave'),
('Maternity','Maternity Leave'),
('Paternity', 'Paternity Leave'),
('Emergency','Emergency Leave'),
('Study','Study Leave'),
)

DAYS = 30


class Leave(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    startdate = models.DateField(default='YYYY-MM-DD', null=True,blank=False)
    enddate = models.DateField(default='YYYY-MM-DD', null=True,blank=False)
    leavetype = models.CharField(choices=LEAVE_TYPE,max_length=25,null=True,blank=False)
    reason = models.CharField(verbose_name=_('Reason for Leave'),max_length=255, null=True,blank=True)
    relievername = models.ForeignKey(User,blank=False, null=True, related_name="reliever",on_delete=models.SET_NULL)     
    maxdays = models.PositiveIntegerField(verbose_name=_('Leave days per year counter'),default=DAYS,null=True,blank=True)
    status = models.CharField(max_length=12,default='pending') #pending,approved,rejected,cancelled
    is_approved = models.BooleanField(default=False) #hide

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LeaveManager()
    
    def __str__(self):
        return str(self.username)


    @property
    def leave_days(self):
        days_count = ''
        startdate = self.startdate
        enddate = self.enddate
        if startdate > enddate:
            return
        dates = (enddate - startdate)
        return dates.days


    @property
    def leave_approved(self):
        return self.is_approved == True


    @property
    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'approved'
            self.save()


    @property
    def unapprove_leave(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()


    @property
    def is_cancelled(self):
        return self.status == 'cancelled'


    @property
    def leaves_cancel(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'cancelled'
            self.save()

    @property
    def uncancel_leave(self):      
        self.is_approved = False
        self.status = 'pending'
        self.save()


    @property
    def reject_leave(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'rejected'
            self.save()

    @property
    def unreject_leave(self):      
        self.is_approved = False
        self.status = 'pending'
        self.save()

    @property
    def is_rejected(self):
        return self.status == 'rejected'