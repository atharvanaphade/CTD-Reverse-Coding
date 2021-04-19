# Imports

from django.db.models.query import QuerySet
from .models import Profile, Question, TestCase, Submission
from .serializers import QuestionSerializer, TestCaseSerializer, AccountSerializer, SubmissionListSerializer, SubmissionDetailSerializer, NewSubmissionSerializer
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from Sandbox import views
from Sandbox.views import Result
import datetime, json, subprocess
import os

# Create your views here.

# Global variables for timer

start_time = 0
end_time = 0
duration = 0
flag = False
start = datetime.datetime(2021, 1, 1, 0, 0)

class QuestionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.create(request, *args, **kwargs)
        return Response({'details': 'You do not have permission to perform this action'}, status=403)

class QuestionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.update(request, *args, **kwargs)
        return Response({'details': 'You do not have permission to perform this action'}, status=403)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        return Response({'details': 'You do not have permission to perform this action'}, status=403)

class TestCaseList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request):
        return self.create(request.data)

class TestCaseDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AccountList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class Timer(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def remaining_time():
        time = datetime.datetime.now()
        now = (time.hour * 60 * 60) + (time.minute * 60) + time.second
        if now < end_time:
            time_left = end_time - now
            return time_left
        else:
            return 0

    def get(self, request):
        if Timer.remaining_time() != 0:
            val = {'status' : 'Remaining time is {}'.format(self.remaining_time())}
            return Response(val, status=201)
        val = {'status' : 'Time is up!'}
        return Response(val, status=201)
    
    @action(methods=['post'], detail=True, permission_classes=[IsAdminUser])
    def post(self, request):
        if request.user.is_superuser:
            global start_time, start
            global end_time
            global duration
            duration = int(request.data['duration'])
            start = datetime.datetime.now()
            start = start + datetime.timedelta(0, 15)
            time = start.second + start.minute * 60 + start.hour * 60 * 60
            start_time = time
            end_time = time + int(duration)
            val = {'status' : 'Time is set! start : {}, remaining_time : {}'.format(start_time, self.remaining_time())}
            return Response(val, status=201)
        return Response({'details': 'You do not have permission to perform this action'}, status=403)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 3

class LeaderBoardListView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_junior_leaderboard(questions, score):

        leaderboard = {}
        for profile in Profile.objects.filter(senior=False).order_by('-total_score', 'latest_submission_time'):
            question_scores = [0 for _ in questions]
            user_submissions = Submission.objects.filter(user_id_fk=profile.user.id)
            if user_submissions:
                for question in questions:
                    question_submission = user_submissions.filter(question_id_fk=question.id)
                    if question_submission:
                        question_score = question_submission.order_by('-score').first()
                        question_scores[question.id - 1] += question_score.score
            question_scores.append(score)
            leaderboard[profile.user.username] = question_scores
        return leaderboard

    @staticmethod
    def get_senior_leaderboard(questions, score):
        leaderboard = {}
        for profile in Profile.objects.filter(senior=True).order_by('-total_score', 'latest_submission_time'):
            question_scores = [0 for _ in questions]
            user_submissions = Submission.objects.filter(user_id_fk=profile.user.id)
            if user_submissions:
                for question in questions:
                    question_submission = user_submissions.filter(question_id_fk=question.id)
                    if question_submission:
                        question_score = question_submission.order_by('-score').first()
                        question_scores[question.id - 1] += question_score.score
            question_scores.append(score)
            leaderboard[profile.user.username] = question_scores
        return leaderboard

    @staticmethod
    def get(request):
        username = request.user.username
        questions = Question.objects.all()
        score = request.user.profile.total_score
        if not request.user.profile.senior:
            leaderboard = LeaderBoardListView.get_junior_leaderboard(questions, score)
        else:
            leaderboard = LeaderBoardListView.get_senior_leaderboard(questions, score)
        rank = int(list(leaderboard.keys()).index(username))
        paginator = Paginator(tuple(leaderboard.items()), 10)  # Show 10 users per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        accuracy = round(((request.user.profile.correct_answers / len(questions)) * 100), 2)
        context = {'username': username, 'rank': rank + 1, 'score': score, 'accuracy': accuracy,
                   'page_range': list(page_range), 'page_obj': page_obj,
        }
        return Response(context, status=201)

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Submission.objects.all()
        return Submission.objects.filter(user_id_fk=self.request.user.pk)

class SubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = SubmissionDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs)
        submission_id = self.kwargs['pk']
        print(self.request.user.is_superuser)
        if self.request.user.is_superuser:
            return Submission.objects.filter(pk=submission_id)
        try:
            queryset = Submission.objects.filter(pk=submission_id, user_id_fk=self.request.user.pk)
        except Submission.DoesNotExist:
            raise exceptions.NotFound(detail="You are not allowed to access this submission")
        return queryset


class Submit(generics.GenericAPIView, mixins.CreateModelMixin):

    serializer_class = NewSubmissionSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, **kwargs):
        # if Timer.remaining_time() != 0:
        user_id_fk = request.user.pk
        profile = Profile.objects.filter(user=request.user)
        question_id_fk = kwargs['pk']
        print(question_id_fk)
        question = Question.objects.filter(id=question_id_fk)
        print(question)
        language = request.data['language'] # get editor language
        code = request.data['code'] # get user code
        attempt = 1  # attempt = 1 by default
        previous_max_marks = 0
        if Submission.objects.filter(user_id_fk=user_id_fk, question_id_fk=question_id_fk).exists(): # check if previously submitted
            submissions = Submission.objects.filter(user_id_fk=user_id_fk, question_id_fk=question_id_fk)
            submission = submissions.order_by('-attempt').first()
            attempt = submission.attempt + 1 # get appropriate attempt number
            submission = submissions.order_by('-score').first()
            previous_max_marks = submission.score

        '''
        we have:

        1. user id fk
        2. question id fk
        3. attempt number
        4. code
        5. language

        call sandbox functions here to get results of submitted code
        '''

        # fetch test case ids and input / output ids

        result_list = {
            'passed_test_cases': [False for _ in TestCase.objects.filter(question_id=question_id_fk)],
            'error': [False for _ in TestCase.objects.filter(question_id=question_id_fk)],
        }
        # tc id, status, err, username, ques id
        index = 0
        for test_case in TestCase.objects.filter(question_id=question_id_fk):
            runner = views.Runner(
                username=request.user.username, 
                lang=language, 
                testcase_id=test_case.id, 
                testcase=test_case.input, 
                testcase_output=test_case.output, 
                ques_id=question_id_fk, 
                code=code, 
                attempt=attempt
            )
            result = runner.RunCode()
            print(result.status)
            if result.status == 'AC':
                print(result_list['passed_test_cases'][index])
                result_list['passed_test_cases'][index] = True
            else:
                result_list['error'][index] = result.error
            index += 1

        print(result_list)

        passed = 0

        for i in result_list['passed_test_cases']:
            if i:
                passed += 1

        question.total_attempts += 1

        if passed == len(TestCase.objects.filter(question_id=question_id_fk)):
            score = question.max_marks
            status = 'PASS'
            accuracy = 100.00
            if not Submission.objects.filter(user_id_fk=user_id_fk, question_id_fk=question_id_fk, status='PASS').exists():
                profile.correct_answers += 1
                question.correct_attempts += 1
        else:
            status = 'FAIL'
            accuracy = round((passed / len(TestCase.objects.filter(question_id=question_id_fk))) * 100, 2)
            # if-else ladder for junior senior marking scheme
            if profile.senior:
                score = 0
            else:
                # logic for junior marking scheme
                score = question.max_marks * (accuracy / 100)
        data = {
            'user_id_fk': user_id_fk,
            'question_id_fk': question_id_fk,
            'score': score,
            'attempt': attempt,
            'status': status,
            'accuracy': accuracy,
            'code': code,
            'language': language
        }
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if score > previous_max_marks:
                profile.total_score -= previous_max_marks
                profile.total_score += score
                # profile.latest_submission_time = datetime.datetime.now()

            question.save()
            profile.save()
            return Response(result_list, status=201)
        else:
            return Response(serializer.errors, status=400)

class LoadBuffer(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, **kwargs):
        question_id = kwargs['pk']
        language = kwargs['ext']
        user = request.user

        buffer = Submission.objects.filter(user_id_fk=user.pk, question_id_fk=question_id, language=language).order_by(
            '-submission_time').first()
        if buffer:
            return Response({'code': buffer.code}, status=201)
        return Response({'details': 'Code not found'}, status=404)

class GetOutput(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = {}  # empty dictionary
        question_id = request.data['pk']
        input = str(request.data['input'])
        result = subprocess.Popen("SandboxData/Executables/Question-{}/a.out".format(question_id),
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (output, error) = result.communicate(input=input.encode())
        data["output"] = output.decode()
        return Response(data, status=201)