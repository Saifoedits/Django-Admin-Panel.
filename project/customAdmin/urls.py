from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('userlogout/', views.user_logout, name='user_logout'),

    path('users/', views.all_users, name='all_users'),
    path('delete/<int:id>', views.user_delete, name='user_delete'),
    path('adduser/', views.add_user, name='add_user'),
    path('edituser/<int:id>', views.edit_user, name='edit_user'),

    path('usergroup/', views.user_group, name='user_group'),
    path('addgroup/', views.add_group, name='add_group'),
    path('deletegroup/<int:id>', views.delete_group, name='delete_group'),
    path('editgroup/<int:id>', views.edit_group, name='edit_group'),

    path('profile/', views.profile, name='profile'),
    path('changepass/', views.change_pass, name='change_pass'),


    path('permissions/', views.permission_list, name='permission_list'),
    path('permissions/add/', views.add_permission, name='add_permission'),
    path('permissions/edit/<int:permission_id>/', views.edit_permission, name='edit_permission'),
    path('permissions/delete/<int:permission_id>/', views.delete_permission, name='delete_permission'),

    path('blog/', views.blogs, name='blogs'),
    path('deleteblog/<int:id>', views.deleteblog, name='deleteblog'),
    path('addblog/', views.add_blog, name='addblog'),
    path('editblog/<int:id>', views.edit_blog, name='editblog'),


    path('category/', views.categories, name='category'),
    path('addcategory/', views.add_category, name='add_category'),
    path('editcategory/<int:id>', views.edit_category, name='edit_category'),
    path('deletecategory/<int:id>', views.delete_category, name='delete_category'),


    path('tags/', views.tags, name='tags'),
    path('addtags/', views.add_tags, name='add_tags'),
    path('edittags/<int:id>', views.edit_tags, name='edit_tags'),
    path('deletetags/<int:id>', views.delete_tags, name='delete_tags'),
    

]

