from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # college = models.CharField(max_length=255)
    total_score = models.FloatField(default=0)
    senior = models.BooleanField(default=False)
    correct_answers = models.IntegerField(default=0)
    latest_submission_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ("profile_" + str(self.pk) + "_" + self.user.username)


class Question(models.Model):
    question_title = models.CharField(max_length=255)
    question_desc = models.TextField("")
    correct_attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    max_marks = models.FloatField(default=0)

    def __str__(self):
        return ("question_" + str(self.pk) + "_" + self.question_title)


class Submission(models.Model):
    user_id_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id_fk = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    submission_time = models.DateTimeField(auto_now=True)
    attempt = models.IntegerField(default=0)
    status = models.CharField(default='NA', max_length=5)
    accuracy = models.FloatField(default=0)

    def __str__(self):
        return("submission_" + str(self.pk) + "_" + self.user_id_fk.username + "_question_" + str(self.question_id_fk))


class TestCase(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    # django supports json field for all databases
    # it is stored as a string in the database but returned as a dictionary in a query

    # input, output, time and memory limits are considered as sets stored in json format
    # input set 1 will have multiple inputs
    # there will be same number of output, time and memory limit entries for 1 test case

    input = models.JSONField()
    output = models.JSONField()
    time_limit = models.JSONField()
    memory_limit = models.JSONField()

    def __str__(self):
        return("test_case_" + str(self.pk) + "_question_" + self.question_id)
