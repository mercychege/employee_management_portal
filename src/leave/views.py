from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from .forms import LeaveCreateForm
from .models import Leave
from employees.models import Employee

# Create your views here.
def leave_create(request):
    if not request.user.is_authenticated:
        return redirect('/')
    submitted = False
    if request.method == 'POST':
        form = LeaveCreateForm(request.POST,request.FILES)
        if form.is_valid():
            leave = form.save(commit=False)
            try:
                leave.username = request.user
            except Exception:
                pass
            leave.save()          
            return HttpResponseRedirect('/leave/apply?submitted=True')
        else:
           messages.info(request, 'Please ensure the dates are correct') 
    else:
        form = LeaveCreateForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'leave/leave_create.html', {'form': form, 'submitted': submitted, 'leave_page':"active"})

class LeaveView(DetailView):
    model = Leave
    context_object_name = 'leave'
 
    def get_context_data(self, **kwargs):
        context = super(LeaveView, self).get_context_data(**kwargs)
        context['leave_page'] ="active"
        return context

def leaves_pending_list(request):
    user = request.user
    context = dict()
    if not request.user.is_authenticated:
        return redirect('/')  
   	
    pending_leaves = Leave.objects.pending_leaves()         
    approved_leaves = Leave.objects.approved_leaves()
    cancelled_leaves = Leave.objects.cancelled_leaves()
    rejected_leaves = Leave.objects.rejected_leaves() 

    user_pending = Leave.objects.pending_leaves().filter(username = user)
    user_approved = Leave.objects.approved_leaves().filter(username = user)
    user_cancelled = Leave.objects.cancelled_leaves().filter(username = user)
    user_rejected = Leave.objects.rejected_leaves().filter(username = user)
    context['pending_leaves'] = pending_leaves     
    context['approved_leaves'] = approved_leaves  
    context['cancelled_leaves'] = cancelled_leaves
    context['rejected_leaves'] = rejected_leaves
    context['user_rejected'] = user_rejected
    context['user_cancelled'] = user_cancelled
    context['user_approved'] = user_approved
    context['user_pending'] = user_pending
    context['leave_page'] = "active"

    return render(request,'leave/leaves_pending.html', context)

def leaves_approved_list(request):
    user = request.user
    context = dict()
    if not request.user.is_authenticated:
        return redirect('/')  
   	
    pending_leaves = Leave.objects.pending_leaves()         
    approved_leaves = Leave.objects.approved_leaves()
    cancelled_leaves = Leave.objects.cancelled_leaves()
    rejected_leaves = Leave.objects.rejected_leaves() 

    user_pending = Leave.objects.pending_leaves().filter(username = user)
    user_approved = Leave.objects.approved_leaves().filter(username = user)
    user_cancelled = Leave.objects.cancelled_leaves().filter(username = user)
    user_rejected = Leave.objects.rejected_leaves().filter(username = user)
    context['pending_leaves'] = pending_leaves     
    context['approved_leaves'] = approved_leaves  
    context['cancelled_leaves'] = cancelled_leaves
    context['rejected_leaves'] = rejected_leaves
    context['user_rejected'] = user_rejected
    context['user_cancelled'] = user_cancelled
    context['user_approved'] = user_approved
    context['user_pending'] = user_pending
    context['leave_page'] = "active"

    return render(request,'leave/leaves_approved.html', context)


def leaves_cancelled_list(request):
    user = request.user
    context = dict()
    if not request.user.is_authenticated:
        return redirect('/')  
   	
    pending_leaves = Leave.objects.pending_leaves()         
    approved_leaves = Leave.objects.approved_leaves()
    cancelled_leaves = Leave.objects.cancelled_leaves()
    rejected_leaves = Leave.objects.rejected_leaves() 

    user_pending = Leave.objects.pending_leaves().filter(username = user)
    user_approved = Leave.objects.approved_leaves().filter(username = user)
    user_cancelled = Leave.objects.cancelled_leaves().filter(username = user)
    user_rejected = Leave.objects.rejected_leaves().filter(username = user)
    context['pending_leaves'] = pending_leaves     
    context['approved_leaves'] = approved_leaves  
    context['cancelled_leaves'] = cancelled_leaves
    context['rejected_leaves'] = rejected_leaves
    context['user_rejected'] = user_rejected
    context['user_cancelled'] = user_cancelled
    context['user_approved'] = user_approved
    context['user_pending'] = user_pending
    context['leave_page'] = "active"

    return render(request,'leave/leaves_cancelled.html', context)

def leaves_rejected_list(request):
    user = request.user
    context = dict()
    if not request.user.is_authenticated:
        return redirect('/')  
   	
    pending_leaves = Leave.objects.pending_leaves()         
    approved_leaves = Leave.objects.approved_leaves()
    cancelled_leaves = Leave.objects.cancelled_leaves()
    rejected_leaves = Leave.objects.rejected_leaves() 

    user_pending = Leave.objects.pending_leaves().filter(username = user)
    user_approved = Leave.objects.approved_leaves().filter(username = user)
    user_cancelled = Leave.objects.cancelled_leaves().filter(username = user)
    user_rejected = Leave.objects.rejected_leaves().filter(username = user)
    context['pending_leaves'] = pending_leaves     
    context['approved_leaves'] = approved_leaves  
    context['cancelled_leaves'] = cancelled_leaves
    context['rejected_leaves'] = rejected_leaves
    context['user_rejected'] = user_rejected
    context['user_cancelled'] = user_cancelled
    context['user_approved'] = user_approved
    context['user_pending'] = user_pending
    context['leave_page'] = "active"

    return render(request,'leave/leaves_rejected.html', context)

def approve_leave(request,id):
    if not request.user.is_authenticated:
        return redirect('/')	
    leave = get_object_or_404(Leave, id = id)
    user = leave.username
    employee = Employee.objects.filter(username = user)[0]
    leave.approve_leave

    messages.error(request,'Leave successfully approved for {0}'.format(employee.username),extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('approvedleavelist')


def unapprove_leave(request,id):
    if not request.user.is_authenticated:
        return redirect('/')	
    leave = get_object_or_404(Leave, id = id)
    leave.unapprove_leave
    return redirect('pendingleavelist')


def cancel_leave(request,id):	
    if not request.user.is_authenticated:
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.leaves_cancel
    messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('cancelledleavelist')


def uncancel_leave(request,id):
    if not request.user.is_authenticated:
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)   
    leave.uncancel_leave
    messages.success(request,'Leave is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('pendingleavelist')

def reject_leave(request,id):
    if not request.user.is_authenticated:
        return redirect('/')
  
    leave = get_object_or_404(Leave, id = id)
    leave.reject_leave
    messages.success(request,'Leave is rejected',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('rejectedleavelist')

def unreject_leave(request,id):
    if not request.user.is_authenticated:
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.unreject_leave
    messages.success(request,'Leave is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('rejectedleavelist')
