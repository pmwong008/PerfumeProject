from django.urls import path

from . import views

app_name = 'ai_app'

urlpatterns = [
    path('question/', views.question, name='question'),
    path('result/',views.result,name='result'),
    path('confirm/', views.confirm, name='confirm'),
    path('order/', views.order, name='order'),

 ]