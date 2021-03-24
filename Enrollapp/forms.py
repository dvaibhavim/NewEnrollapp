from django import forms
from Enrollapp.models import UserProfileInfo
from django.contrib.auth.models import User
from dobwidget import DateOfBirthWidget

'''
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('email',)'''
class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('gender','date_of_birth','Role','standard')
         widgets = {
            'date_of_birth': DateOfBirthWidget(order='DMY'),
        }
