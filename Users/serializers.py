from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Question, TestCase, Profile
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title', 'question_desc', 'correct_attempts', 'total_attempts', 'max_marks']


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['question_id', 'input', 'output', 'time_limit', 'memory_limit']

class AccountSerializer(serializers.ModelSerializer):
    class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            exclude = ['user']
    
    profile = ProfileSerializer()
    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_staff', 'date_joined', 'is_active', 'groups', 'user_permissions']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user_instance = User.objects.create(**validated_data)
        Profile.objects.create(user=user_instance, **profile_data)
        return user_instance