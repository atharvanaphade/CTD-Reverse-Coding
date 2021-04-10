from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=255)
    total_score = models.IntegerField(default=0)
    junior = models.BooleanField(default=False)
    correct_answered = models.IntegerField(default=0)
    latest_submission_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    ques_title = models.CharField(max_length=255)
    ques_desc = models.TextField("")
    successful_attempts = models.IntegerField(default=0)
    number_of_attempts = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.ques_title

class Submissions(models.Model):
    ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    attempt = models.IntegerField(default=0)
    status = models.CharField(default='NA', max_length=5)
    submission_time = models.CharField(default="", max_length=15)
    score = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Submissions'
        verbose_name_plural = 'Submissions'
    
    def __str__(self):
        return(self.pk + " - question-" + str(self.ques_id.pk))

class MultipleUserSubmission(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_id = models.ForeignKey(Submissions, on_delete=models.CASCADE)

    def __str__(self):
        return(self.user_id.username + "-" + self.submission_id)

class TestCase(models.Model):
    ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    time_limit = models.IntegerField(default=2)
    mem_limit = models.IntegerField(default=64000000)
    

class Input(models.Model):
    tc_id = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    input = models.TextField("")

class Output(models.Model):
    tc_id = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    output = models.TextField("")