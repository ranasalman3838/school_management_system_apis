from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Teacher, Course, Student, Assessment ,EnrollmentAssessment,Invitation,Enrollment
from .serializers import AdminTeacherSerializer, AdminCourseSerializer, AdminStudentSerializer, AdminInviteAssessmentSerializer,TeacherSerializer,TeacherStudentSerializer,TeacherCourseSerializer,TeacherAssessmentSerializer,TeacherAssessmentDetailSerializer,StudentSerializer, StudentCourseSerializer, StudentAssessmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class AdminTeacherListCreateView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = AdminTeacherSerializer
    permission_classes = [IsAdminUser]

class AdminTeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = AdminTeacherSerializer
    permission_classes = [IsAdminUser]

class AdminCourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = AdminCourseSerializer
    permission_classes = [IsAdminUser]

class AdminCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = AdminCourseSerializer
    permission_classes = [IsAdminUser]

class AdminStudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = AdminStudentSerializer
    permission_classes = [IsAdminUser]

class AdminStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = AdminStudentSerializer
    permission_classes = [IsAdminUser]

class AdminInviteAssessmentView(generics.GenericAPIView):
    serializer_class = AdminInviteAssessmentSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        assessment = Assessment.objects.create(
            course=serializer.validated_data['course'],
            date=serializer.validated_data['date']
        )
        assessment.students.set(serializer.validated_data['students'])
        assessment.save()
        return Response({'status': 'Assessment invited successfully'}, status=status.HTTP_201_CREATED)


# views.py


class TeacherListCreateAPIView(ListCreateAPIView):
    """
    API view to get the list of teachers or create a new teacher.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class TeacherDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a teacher instance.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class TeacherStudentListCreateAPIView(ListCreateAPIView):
    """
    API view to get the list of students created by the teacher or create a new student.
    """
    serializer_class = TeacherStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(teacher=self.request.user.teacher)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)

class TeacherStudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a student instance created by the teacher.
    """
    serializer_class = TeacherStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(teacher=self.request.user.teacher)

class TeacherCourseListCreateAPIView(ListCreateAPIView):
    """
    API view to get the list of courses created by the teacher or create a new course.
    """
    serializer_class = TeacherCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user.teacher)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)

class TeacherCourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a course instance created by the teacher.
    """
    serializer_class = TeacherCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user.teacher)

class TeacherAssessmentListCreateAPIView(ListCreateAPIView):
    """
    API view to get the list of assessments created by the teacher or create a new assessment.
    """
    serializer_class = TeacherAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assessment.objects.filter(course__teacher=self.request.user.teacher)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)

class TeacherAssessmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete an assessment instance created by the teacher.
    """
    serializer_class = TeacherAssessmentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assessment.objects.filter(course__teacher=self.request.user.teacher)


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentCourseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user.student)

    def perform_create(self, serializer):
        student = self.request.user.student
        course = serializer.validated_data['course']
        Enrollment.objects.create(student=student, course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentCourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user.student)


class StudentAssessmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StudentAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assessment.objects.filter(
            course__students=self.request.user.student,
            date__gte=self.request.query_params.get('start_date', '2000-01-01'),
            date__lte=self.request.query_params.get('end_date', '3000-01-01'),
        )

    def perform_create(self, serializer):
        student = self.request.user.student
        assessment = serializer.validated_data['assessment']
        EnrollmentAssessment.objects.create(student=student, assessment=assessment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentAssessmentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = StudentAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assessment.objects.filter(
            course__students=self.request.user.student,
            date__gte=self.request.query_params.get('start_date', '2000-01-01'),
            date__lte=self.request.query_params.get('end_date', '3000-01-01'),
        )
