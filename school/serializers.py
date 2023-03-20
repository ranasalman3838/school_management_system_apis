from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Teacher, Course, Student, Assessment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            teacher = Teacher.objects.create(user=user, **validated_data)
            return teacher


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            student = Student.objects.create(user=user, **validated_data)
            return student


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'


class AdminTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            teacher = Teacher.objects.create(user=user, **validated_data)
            return teacher


class AdminCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AdminStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            student = Student.objects.create(user=user, **validated_data)
            return student


class AdminInviteAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ('id', 'title', 'description', 'start_datetime', 'end_datetime', 'course', 'students')

    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = Assessment
        fields = ('id', 'name', 'description', 'course', 'course_name', 'student', 'student_name', 'date', 'marks')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TeacherStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TeacherCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TeacherAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'course', 'scheduled_date']


class TeacherAssessmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentCourseSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer(read_only=True)
        return super().to_representation(instance)


class StudentAssessmentSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Assessment
        exclude = ('students',)

        