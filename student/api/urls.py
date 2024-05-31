from django.urls import path, include
from . views import StudentAPI, student_create, student_update, student_delete, student_list
# Add more URL patterns here

urlpatterns = [
    path('student/', StudentAPI.as_view(), name= 'student'),
    path('', student_list, name='student_list'),
    path('students/create/', student_create, name='student_create'),
    path('students/update/<int:pk>/', student_update, name='student_update'),
    path('students/delete/<int:pk>/', student_delete, name='student_delete'),
]
