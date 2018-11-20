from django import forms

from pagedown.widgets import PagedownWidget
from .models import Postgroup

class PostGroupForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = Postgroup
		fields = [
			"title",
			"posts",
			"teaser",
			"content",
			"image",
			"draft",
			"publish",
		]