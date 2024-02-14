from django.contrib import admin
from django.urls import path,include
from crudapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('student-api/',views.StudentApi.as_view(),name='studentapi'),
    path('student-api/<int:pk>/',views.StudentApi.as_view(),name='studentapi'),
]
