from django.urls import path
from connect.views import EligibilityChecksAPIView

urlpatterns = [
    path('user_eligibility_check/', EligibilityChecksAPIView.as_view()),
]