from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from .views import QuestionViewSet, RegisterView,LogoutView



router = DefaultRouter()
router.register(r'api/questions',QuestionViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Medical Quiz API",
        default_version="v1",
        description="API documentation for the Medical Quiz system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@quizapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('',include(router.urls)),
    # path('questions/', QuestionListView.as_view(), name='question-list'),
    path('api/register/',RegisterView.as_view(),name='register'),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('api/logout/',LogoutView.as_view(),name='logout'),
    
    #Swagger documentation
    re_path(r'^swagger/$',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    

]
