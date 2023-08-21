from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from .models import blog
from .models import category
from .models import tag


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        # add custom input fields in form
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active','is_superuser','groups']
        # change form input names
        labels = {'email': 'Email'}

class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']
        labels = {'email': 'Email'}        

class EditAdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active','is_superuser','groups']
        labels = {'email': 'Email'}        


class GroupPermissionsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['permissions']
        

class GroupPermissionsForm2(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['permissions', 'name']        


class CustomPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'codename', 'content_type']


choices = category.objects.all().values_list('name', 'name')
choices2 = tag.objects.all().values_list('name', 'name')

choice_list = []
choice_list2 = []

for item in choices:
    choice_list.append(item)

for item in choices2:
    choice_list2.append(item)


class BlogForm(forms.ModelForm):
    class Meta:
        model = blog
        fields = ['cover', 'title', 'content', 'slug', 'category', 'tag']

        widgets = {
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'tag': forms.Select(choices=choice_list2, attrs={'class': 'form-control'}),
        }


class categoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = ['name', 'parent'] 

class tagForm(forms.ModelForm):
    class Meta:
        model = tag
        fields = ['name']
        labels = {'name':'Tag Name'} 

