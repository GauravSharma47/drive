from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*,video/*'}))
    # name = forms.CharField(max_length=40)

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user