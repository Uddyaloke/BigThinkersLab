from django import forms

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")		
		# user_qs = User.objects.filter(username=username)
		# if user_qs.count() == 1:
		# 	user = user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user doesnot exist??")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password?")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active?")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email address')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]

	# def clean(self, *args, **kwargs):
	# 	email = self.cleaned_data.get("email")
	# 	email2 = self.cleaned_data.get("email2")
	# 	if email != email2:
	# 		raise forms.ValidationError("Emails must match")

	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("This email has already been registered")

	# 	return super(UserRegisterForm, self).clean(*args, **kwargs)


	def clean_email2(self):
		# print(self.cleaned_data)
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		# print(email, email2)
		if email != email2:
			raise forms.ValidationError("Emails must match")

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")

		return email



