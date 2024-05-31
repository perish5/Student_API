from django.shortcuts import render, redirect
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from rest_framework.views import APIView
# Create your views here.

class StudentAPI(APIView):
    
    
    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs, many=True)
        return Response({'status': 200 , 'payload': serializer.data})

    
    def post(self, request):
        serializer = StudentSerializer(data = request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403 , 'error' :serializer.errors, 'message' : 'Something went wrong.'})
        serializer.save()
        return Response({'status': 200, 'payload': serializer.data , 'message': 'Your data sent.'})

        
    def patch(self, request):
        try:
            student_obj = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(instance = student_obj, data = request.data, partial = True)
            
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
            serializer.save()
            
            return Response({'status': 200, 'payload': serializer.data, 'message':'Your data has been updates..'})
        
        except Student.DoesNotExist:
            return Response({'status': 404, 'message': 'Invalid ID. Student not found.'})
        except Exception as e:
            return Response({'status': 500, 'message': str(e)})
    
    def delete(self, request):
        try:
            student_obj = Student.objects.get(id = request.data['id'])
            student_obj.delete()
            return Response({'status': 200, 'message': 'Item Deleted Successfully.'})
            
        except Exception as e:
            return Response({'status': 403, 'message': 'Invalid ID.'})
 

# students/views.py (continued)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from django.views.decorators.http import require_http_methods


def student_create(request):
    if request.method == 'POST':
        Student.objects.create(
            name=request.POST['name'],
            age=request.POST['age'],
            address=request.POST['address'],
            grade=request.POST['grade'],
            major=request.POST['major']
        )
        return redirect('student_list')
    return render(request, 'student_form.html', {'form_title': 'Add Student', 'student': {}})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.age = request.POST['age']
        student.address = request.POST['address']
        student.grade = request.POST['grade']
        student.major = request.POST['major']
        student.save()
        return redirect('student_list')
    return render(request, 'student_form.html', {'form_title': 'Edit Student', 'student': student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})
