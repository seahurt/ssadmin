from django import forms
from .models import SSRecord

class SSForm(forms.ModelForm):
	class Meta:
		model = SSRecord
		fields = ['port','passwd','encode']
