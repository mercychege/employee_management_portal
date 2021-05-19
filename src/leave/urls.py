from django.urls import path
from . import views
from .views import LeaveView


 
urlpatterns = [		
	path('view/<int:pk>', LeaveView.as_view(), name='leave-detail'),
	path('apply/', views.leave_create, name= 'leave-application'),
	path('pending/all/',views.leaves_pending_list,name='pendingleavelist'),
	path('approved/all/',views.leaves_approved_list,name='approvedleavelist'),
	path('cancelled/all/',views.leaves_cancelled_list,name='cancelledleavelist'),
	path('rejected/all/',views.leaves_rejected_list,name='rejectedleavelist'),
	path('approve/<int:id>',views.approve_leave,name='approve'),
    path('unapprove/<int:id>',views.unapprove_leave,name='unapprove'),
	path('cancel/<int:id>',views.cancel_leave,name='cancel'),
	path('uncancel/<int:id>',views.uncancel_leave,name='uncancel'),
    path('reject/<int:id>',views.reject_leave,name='reject'),
	path('unreject/<int:id>',views.unreject_leave,name='unreject'),
    
]