from django import forms
from .models import Leave
import datetime


class DateInput(forms.DateInput):
    input_type= 'date'

class LeaveCreateForm(forms.ModelForm):
	reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
	class Meta:
		model = Leave
		exclude = ['username','maxdays','status','is_approved','updated','created']
		widgets = {'startdate': DateInput(), 'enddate': DateInput()}
	
	def clean_enddate(self):
		enddate = self.cleaned_data['enddate']
		startdate = self.cleaned_data['startdate']
		today_date = datetime.date.today()

		if (startdate or enddate) < today_date:
			raise forms.ValidationError("")

		elif startdate >= enddate:
			raise forms.ValidationError("")

		return enddate