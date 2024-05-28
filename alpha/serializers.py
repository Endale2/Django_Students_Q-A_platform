from rest_framework import serializers
from .models import*
from django.contrib.auth import authenticate

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'  # Include all fields

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)  # Nested serialization

    class Meta:
        model = Course
        fields = ( 'course', 'department')  # Explicit field selection

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = '__all__'  # Include all fields

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["phone_number",
            "status"] # Customize user fields



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'department', 'status']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "phone_number" and "password" fields.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class QuestionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    course = CourseSerializer()
    hashtags = HashTagSerializer(many=True)

    class Meta:
        model = Questions
        fields = ('user', 'date', 'department', 'course', 'question', 'hashtags')


class AnswerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Answers
        fields = ('user', 'answer', 'date')


class ReplySerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Replies
        fields = ('user', 'reply', 'date')

class QuestionDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    course = CourseSerializer()
    user = CustomUserSerializer()
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ('question', 'id', 'user', 'date', 'department', 'course', 'hashtags', 'answers')

    
