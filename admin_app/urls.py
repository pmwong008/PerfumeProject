from django.urls import path

from . import views

app_name = 'admin_app'

urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path('profile/',views.profile,name='profile'),
    path('account/delete/', views.delete_account, name='delete_account'),

 ]