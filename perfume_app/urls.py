from django.urls import path

from . import views

app_name = 'perfume_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_guide',views.user_guide,name='user_guide'),
    path('perfumes_list/',views.perfumes_list,name='perfumes_list'),
    path('perfume/<int:pk>',views.perfume_detail,name='perfume_detail'),
    path('perfume/<int:pk>/review',views.submit_review,name='submit_review'),

 ]