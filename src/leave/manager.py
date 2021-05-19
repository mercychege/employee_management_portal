from django.db import models
import datetime

class LeaveManager(models.Manager):
	def get_queryset(self):
		'''
		overrides objects.all() 
		return all leaves including pending or approved
		'''
		return super().get_queryset()


	def pending_leaves(self):
		return super().get_queryset().filter(status = 'pending').order_by('-created')

	def approved_leaves(self):
		return super().get_queryset().filter(status = 'approved').order_by('-created')

	def cancelled_leaves(self):
		return super().get_queryset().filter(status = 'cancelled').order_by('-created')


	def rejected_leaves(self):
		return super().get_queryset().filter(status = 'rejected').order_by('-created')


	def current_year_leaves(self):
		'''
		returns all leaves in current year; Leave.objects.all_leaves_current_year()
		or add all_leaves_current_year().count() -> int total 
		this include leave approved,pending,rejected,cancelled

		'''
		return super().get_queryset().filter(startdate__year = datetime.date.today().year)



