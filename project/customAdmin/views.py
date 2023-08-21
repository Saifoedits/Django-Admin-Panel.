from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm,EditUserProfileForm,EditAdminProfileForm
from django.contrib.auth.models import Group
from .forms import GroupPermissionsForm2
from .forms import GroupPermissionsForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomPermissionForm
from django.contrib.auth.models import Permission
from .models import blog
from .forms import BlogForm
from .forms import categoryForm
from .models import category
from .models import tag
from .forms import tagForm





# Create your views here.

def user_login(request):
     if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                username = fm.cleaned_data['username']
                userpassword = fm.cleaned_data['password']
                user = authenticate(username=username, password=userpassword)
            if user is not None:
                messages.success(request, 'Logged in Successfully!')
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = AuthenticationForm()
        return render(request, 'pages/login.html', {'form': fm})
     else:
      return HttpResponseRedirect('/dashboard/')

@login_required(login_url='/') #redirect when user is not logged in
def dashboard(request):
    return render(request, 'pages/dashboard.html')


def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')


# Users

@login_required(login_url='/') 
@permission_required('customAdmin.view_all_users', raise_exception=True)  #adding permissions
def all_users(request):
        users = User.objects.all()
        return render(request, 'pages/all_users.html', {'users': users})


@permission_required('customAdmin.delete_user', raise_exception=True)  #adding permissions
@login_required(login_url='/')     
def user_delete(request, id):
    fm = User.objects.get(id=id)
    fm.delete()
    return HttpResponseRedirect('/users')   


@login_required(login_url='/') 
def add_user(request):
        if request.method == "POST": 
            fm = SignUpForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Account Created Successfully')  
            else:
                messages.error(request, 'Please fill all fields correctly !!')   
        else:
            fm = SignUpForm
        return render(request, 'pages/adduser.html', {'form': fm})


@login_required(login_url='/')     
def edit_user(request, id):
            if request.method == 'POST':
                pi = User.objects.get(pk=id)
                fm = EditAdminProfileForm(request.POST, instance=pi)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Profile Updated')
            else:
                pi = User.objects.get(pk=id)
                fm = EditAdminProfileForm(instance=pi)       
            return render(request, 'pages/edituser.html', {'form': fm})
        
# Group

@login_required(login_url='/') 
def user_group(request):
        fm = Group.objects.all()
        return render(request, 'pages/usergroup.html', {'form': fm})


@login_required(login_url='/') 
def delete_group(request, id):
        fm = Group.objects.get(id=id)
        fm.delete()
        return HttpResponseRedirect('/usergroup')
   

@login_required(login_url='/') 
def add_group(request):
        if request.method == 'POST':
            form = GroupPermissionsForm2(request.POST)
            if form.is_valid():
                group = form.save()  # Save the group with its permissions
                messages.success(request, 'Group created successfully.')
                return redirect('user_group')  # Redirect to the group list view or any other appropriate view
        else:
            form = GroupPermissionsForm2()
        
        return render(request, 'pages/addgroup.html', {'form': form})

    
@login_required(login_url='/') 
def edit_group(request, id):
    group = Group.objects.get(id=id)
    permissions = group.permissions.all()

    if request.method == 'POST':
        form = GroupPermissionsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permissions updated successfully.')
    else:
        form = GroupPermissionsForm(instance=group)
    return render(request, 'pages/editgroup.html', {'group': group, 'permissions': permissions, 'form': form})


@login_required(login_url='/') 
def profile(request):
    username = request.user.username  # Retrieve the username

    if request.method == 'POST':
        if request.user.is_superuser:
            fm = EditAdminProfileForm(request.POST, instance=request.user)
        else:
            fm = EditUserProfileForm(request.POST, instance=request.user)

        if fm.is_valid():
            fm.save()
            messages.success(request, 'Your Profile is Updated')
            return redirect('profile')  # Redirect after successful form submission
    else:
        if request.user.is_superuser:
            fm = EditAdminProfileForm(instance=request.user)
        else:
            fm = EditUserProfileForm(instance=request.user)
        return render(request, 'pages/profile.html', {'form': fm, 'username': username})
   

@login_required(login_url='/')    
def change_pass(request):
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Changed Successfully') 
                return HttpResponseRedirect('/admin/')
        else:    
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'pages/changepass.html', {'form': fm})



# custom permissions


@login_required(login_url='/') 
def permission_list(request):
        permissions = Permission.objects.all()
        return render(request, 'pages/permissions/permission_list.html', {'permissions': permissions})


@login_required(login_url='/') 
def add_permission(request):
        if request.method == 'POST':
            form = CustomPermissionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('permission_list')
        else:
            form = CustomPermissionForm()
        return render(request, 'pages/permissions/add_permission.html', {'form': form})
   

@login_required(login_url='/')    
def edit_permission(request, permission_id):
        permission = get_object_or_404(Permission, pk=permission_id)
        if request.method == 'POST':
            form = CustomPermissionForm(request.POST, instance=permission)
            if form.is_valid():
                form.save()
                return redirect('permission_list')
        else:
            form = CustomPermissionForm(instance=permission)
        return render(request, 'pages/permissions/edit_permission.html', {'form': form, 'permission': permission})
 
@login_required(login_url='/')  
def delete_permission(request, permission_id):
        permission = get_object_or_404(Permission, pk=permission_id)
        permission.delete()
        return redirect('permission_list')



# Blogs

def blogs(request):
    all_blog = blog.objects.all()
    return render(request, 'pages/blogs/blog.html', {'blog': all_blog})

def deleteblog(request, id):
    delete = blog.objects.get(id=id).delete()
    return HttpResponseRedirect('/blog/')


def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():  # Check if the categoryForm is valid too
            form.save()
            messages.success(request, 'Blog Added Successfully')
            return redirect('/blog')
    else:
        form = BlogForm()

    return render(request, 'pages/blogs/addblog.html', {'form': form})


def edit_blog(request, id):
    if request.method == 'POST':
        pi = blog.objects.get(id=id)
        fm = BlogForm(request.POST, instance=pi)
        if fm.is_valid:
            fm.save()
            messages.success(request, 'Blog Updated')
    else:
        pi = blog.objects.get(id=id)
        fm = BlogForm(instance=pi)       
    return render(request, 'pages/blogs/editblog.html', {'form': fm})



# Categories

def categories(request):
    fm = category.objects.all()
    return render(request, 'pages/category/category.html', {'form':fm})

def add_category(request):
    if request.method == 'POST':
        fm = categoryForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Category added')
            return redirect('category')
        else:
            messages.error(request, 'Error')
    else:
        fm = categoryForm(request.POST)
    return render(request, 'pages/category/addcategory.html', {'form':fm})
    

def delete_category(request, id):
    fm = category.objects.get(id=id).delete()
    return HttpResponseRedirect('/category/')
     

def edit_category(request, id):
    pi =  category.objects.get(id=id)
    
    if request.method == 'POST':
        fm = categoryForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Category Updated')
        else:
            messages.error(request, 'Error')
    else:
        fm = categoryForm(instance=pi)
    
    return render(request, 'pages/category/editcategory.html', {'form': fm})
    


# tags

def tags(request):
    fm = tag.objects.all()
    return render(request, 'pages/tags/tags.html', {'form': fm})

def add_tags(request):
    if request.method == "POST": 
        fm = tagForm(request.POST)
        if fm.is_valid:
            fm.save()
            messages.success(request, 'Tag Added Successfully')
            return redirect('/tags')
    else:
        fm = tagForm(request.POST)
    return render(request, 'pages/tags/addtags.html', {'form': fm})

def edit_tags(request, id):
    pi = tag.objects.get(id=id)

    if request.method == 'POST':
        fm = tagForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Tag Updated')
        else:
            messages.error(request, 'Error')   
    else:
        fm = tagForm(instance=pi)
    return render(request, 'pages/tags/edittags.html', {'form': fm})

def delete_tags(request, id):
    fm = tag.objects.get(id=id).delete()
    return HttpResponseRedirect('/tags/')

