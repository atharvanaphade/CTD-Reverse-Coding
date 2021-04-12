from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Users import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('questions/', views.QuestionList.as_view()),
    path('questions/<int:pk>/', views.QuestionDetail.as_view()),
    path('testcases/', views.TestCaseList.as_view()),
    path('testcases/<int:pk>', views.TestCaseDetail.as_view()),
    path('profiles/', views.AccountList.as_view()),
    path('profiles/<int:pk>', views.AccountDetail.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view()),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


