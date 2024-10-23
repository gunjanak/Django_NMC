from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import QuestionViewSet, RegisterView,LogoutView



router = DefaultRouter()
router.register(r'api/questions',QuestionViewSet)

urlpatterns = [
    path('',include(router.urls)),
    # path('questions/', QuestionListView.as_view(), name='question-list'),
    path('api/register/',RegisterView.as_view(),name='register'),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('api/logout/',LogoutView.as_view(),name='logout'),
]
