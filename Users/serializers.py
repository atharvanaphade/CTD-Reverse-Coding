from django.db.models import fields
from rest_framework import serializers
from .models import Question, TestCase

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title', 'question_desc', 'correct_attempts', 'total_attempts', 'max_marks']


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['question_id', 'input', 'output', 'time_limit', 'memory_limit']
