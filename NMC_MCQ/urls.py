from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import QuestionListView, QuestionViewSet


router = DefaultRouter()
router.register(r'question',QuestionViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('questions/', QuestionListView.as_view(), name='question-list'),
]
