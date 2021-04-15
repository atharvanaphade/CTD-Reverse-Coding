# Imports
from django.db.models.query import QuerySet
from .models import Profile, Question, TestCase, Submission
from .serializers import QuestionSerializer, TestCaseSerializer, AccountSerializer, SubmissionSerializer
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
import datetime

# Create your views here.

# Variable Declaration
start_time = 0
end_time = 0
duration = 0
flag = False
start = datetime.datetime(2021, 1, 1, 0, 0)

class QuestionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class QuestionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TestCaseList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

    def create(self, data, *args, **kwargs):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        input_json = {}
        output_json = {}
        input = data['input']
        output = data['output']
        counter = 1
        for inp in input.split(' '):
            if inp.isdigit():
                input_json['{}'.format(counter)] = inp
            counter = counter + 1
        counter = 1
        for out in output.split(' '):
            if out.isdigit():
                output_json['{}'.format(counter)] = out
            counter = counter + 1
        data['input'] = input_json
        data['output'] = output_json
        return self.create(data, *args, **kwargs)

class TestCaseDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AccountList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

class Timer(APIView):
    def remaining_time(self):
        time = datetime.datetime.now()
        now = (time.hour * 60 * 60) + (time.minute * 60) + time.second
        if now < end_time:
            time_left = end_time - now
            return time_left
        else:
            return 0

    def get(self, request, format=None):
        if self.remaining_time() != 0:
            val = {'status' : 'Remaining time is {}'.format(self.remaining_time())}
            return Response(val, status=201)
        val = {'status' : 'Timer is not set'}
        return Response(val, status=201)
    
    @action(methods=['post'], detail=True, permission_classes=[IsAdminUser])
    def post(self, request, format=None):
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

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 3

class LeaderBoardListView(generics.ListAPIView):
    queryset = User.objects.order_by('-profile__total_score')
    serializer_class = AccountSerializer
    pagination_class = StandardResultsSetPagination

    # def get(self, request, format=None):
    #     questions = Question.objects.all()
    #     current_user = request.user.username
    #     current_score = request.user.profile.total_score
    #     leaderboard = {}
    #     for profile in Profile.objects.order_by('-total_score'):
    #         question_scores = [0 for i in questions]
    #         user_submissions = Submission.objects.filter(user_id_fk=profile.user.id)
    #         if user_submissions:
    #             for question in questions:
    #                 question_submission = user_submissions.filter(pk=question.id)
    #                 if question_submission:
    #                     question_score = question_submission.order_by('-score').first()
    #                     question_scores[question.id - 1] += question_score.score
    #         question_scores.append(profile.total_score)
    #         leaderboard[profile.user.username] = question_scores
    #     rank = int(list(leaderboard.keys()).index(current_user))
    #     paginator = Paginator(tuple(leaderboard.items()), 10)  # Show 10 users per page.
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     page_range = paginator.page_range
    #     user_accuracy = round(((request.user.profile.correct_answers / len(questions)) * 100), 2)
    #     context = {'current_user': current_user, ''
    #                 'current_user_score': current_score, 'current_user_rank': rank + 1,
    #                 'user_accuracy': user_accuracy}
    #     return Response(context, status=201)

class SubmissionListView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    # def post(self, request, *args, **kwargs):
    #     data = request.data

    #     pass

class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

   

