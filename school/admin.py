from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assessment)
admin.site.register(EnrollmentAssessment)
admin.site.register(Invitation)
