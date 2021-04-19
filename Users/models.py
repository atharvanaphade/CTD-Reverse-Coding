from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.FloatField(default=0)
    senior = models.BooleanField(default=False)
    correct_answers = models.IntegerField(default=0)
    latest_submission_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "profile_" + str(self.pk) + "_" + self.user.username


class Question(models.Model):
    question_title = models.CharField(max_length=255)
    question_desc = models.TextField(default="")
    correct_attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    max_marks = models.FloatField(default=0)

    def __str__(self):
        return "question_" + str(self.pk) + "_" + self.question_title


class Submission(models.Model):

    languages = [("cpp", "C++"), ("c", "C"), ("py", "Python"), ("java", "Java")]

    user_id_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id_fk = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    submission_time = models.DateTimeField(auto_now=True)
    attempt = models.IntegerField(default=0)
    status = models.CharField(default='NA', max_length=5)
    accuracy = models.FloatField(default=0)
    code = models.TextField(default="")
    language = models.CharField(max_length=6, choices=languages)

    def __str__(self):
        return "submission_" + str(self.pk) + "_" + self.user_id_fk.username + "_question_" + str(self.question_id_fk)


class TestCase(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()

    def __str__(self):
        return "test_case_" + str(self.pk) + "_question_" + str(self.question_id)