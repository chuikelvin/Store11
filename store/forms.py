from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from.models import User

# class UserForm(ModelForm):
#     # username = forms.CharField(label='subject', 
#     #                       max_length=100,
#     #                       widget=forms.TextInput(
#     #                           attrs={'class': "form-control",'placeholder':"ent use"}))
#     # email = forms.EmailField(max_length=60, help_text = 'Required. Add a valid email address')
#     # password =forms.CharField(widget=forms.PasswordInput)
#     password =forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         # fields = '__all__'
#         fields = ['username','password', 'first_name','last_name']

# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model =