from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Question, Submission, TestCase, Profile
from django.contrib.auth.models import User
from Sandbox import imports
import os

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['correct_attempts', 'total_attempts']


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):

    class ProfileSerializer(serializers.ModelSerializer):
        senior = serializers.NullBooleanField()
        class Meta:
            model = Profile
            fields = ['senior']
    
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']
    
    @staticmethod
    def create(validated_data):
        print(type(validated_data))
        user_instance = User.objects.create_user(**validated_data)
        if 'profile' in validated_data.keys():
            profile_data = validated_data.pop('profile')
            Profile.objects.create(user=user_instance, **profile_data)
        else:
            Profile.objects.create(user=user_instance)
        users_folder = '../SandboxData/Users/{}/{}/{}/'
        languages = ['java', 'py', 'c', 'cpp']
        os.chdir(imports.cur_dir)
        for ques in Question.objects.all():
            for i in range(len(languages)): 
                os.makedirs(users_folder.format(user_instance.username, ques.pk, languages[i]), 0o755)
                os.chdir(users_folder.format(user_instance.username, ques.pk, languages[i]))
                # code_file = open("main.{}".format(self.lang), "w+")
                # code_file.close()
                dockerfile = open("Dockerfile", "w+")
                dockerfile.write(imports.Dockerfile[i])
                dockerfile.close()
                entrypointfile = open("entrypoint.sh", "w+")
                entrypointfile.write(imports.EntryPointScript[i])
                entrypointfile.close()
                input_file = open("input", "w+")
                input_file.close()
                output_file = open("output", "w+")
                output_file.close()
                os.chdir(imports.cur_dir)
        return user_instance

class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['pk', 'submission_time', 'accuracy']

class SubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['language', 'code']

class NewSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
