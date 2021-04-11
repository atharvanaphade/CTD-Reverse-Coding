from django.db.models import fields
from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title', 'question_desc', 'correct_attempts', 'total_attempts', 'max_marks']

