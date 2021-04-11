from django.contrib import admin
from .models import (
    Profile,
    Question,
    Submission,
    TestCase,
)

# Register your models here.

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(TestCase)