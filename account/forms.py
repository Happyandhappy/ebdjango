from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import UserProfile
from django.contrib.auth import password_validation

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)

        if password != confirm_password:
            self._errors['password'] = self._errors.get('password', [])
            self._errors['password'].append("passwords does not match")

        return cleaned_data


class EditProfileForm(UserChangeForm):
    template_name='/account/edit_profile.html'

    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )
