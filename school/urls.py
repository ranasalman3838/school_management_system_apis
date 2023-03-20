from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [

    # Admin Routes
    path('admin/teachers/', AdminTeacherListCreateView.as_view(), name='admin-teacher-list-create'),
    path('admin/teachers/<int:pk>/', AdminTeacherDetailView.as_view(), name='admin-teacher-detail'),
    path('admin/courses/', AdminCourseListCreateView.as_view(), name='admin-course-list-create'),
    path('admin/courses/<int:pk>/', AdminCourseDetailView.as_view(), name='admin-course-detail'),
    path('admin/students/', AdminStudentListCreateView.as_view(), name='admin-student-list-create'),
    path('admin/students/<int:pk>/', AdminStudentDetailView.as_view(), name='admin-student-detail'),
    path('admin/invite-assessment/', AdminInviteAssessmentView.as_view(), name='admin-invite-assessment'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),


   # Teacher Routes
    path('teacher/login/', TokenObtainPairView.as_view(), name='teacher-login'),
    path('teacher/refresh/', TokenRefreshView.as_view(), name='teacher-refresh'),
    path('teacher/', TeacherListCreateAPIView.as_view(), name='teacher-list'),
    path('teacher/<int:pk>/students/', TeacherDetailAPIView.as_view(), name='teacher-student-list'),
    path('teacher/<int:pk>/students/<int:student_id>/', TeacherStudentDetailAPIView.as_view(), name='teacher-student-detail'),
    path('teacher/<int:pk>/courses/', TeacherCourseListCreateAPIView.as_view(), name='teacher-course-list'),
    path('teacher/<int:pk>/courses/<int:course_id>/', TeacherCourseDetailAPIView.as_view(), name='teacher-course-detail'),
    path('teacher/<int:pk>/assessments/', TeacherAssessmentListCreateAPIView.as_view(), name='teacher-assessment-list'),
    path('teacher/<int:pk>/assessments/<int:assessment_id>/', TeacherAssessmentDetailAPIView.as_view(), name='teacher-assessment-detail'),

     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('students/', StudentListCreateAPIView.as_view(), name='students'),
    path('students/<int:pk>/courses/', StudentDetailAPIView.as_view(), name='student_courses'),
    path('students/<int:pk>/courses/<int:course_id>/', StudentCourseDetailAPIView.as_view(), name='student_course_detail'),
    path('students/<int:pk>/assessments/', StudentAssessmentListCreateAPIView.as_view(), name='student_assessments'),
    path('students/<int:pk>/assessments/<int:assessment_id>/', StudentAssessmentDetailAPIView.as_view(), name='student_assessment_detail'),



]