from django.urls import path

from study_platform.apps import StudyPlatformConfig
from rest_framework.routers import DefaultRouter

from study_platform.views import CourseViewSet, SubjectCreateAPIView, SubjectListAPIView, SubjectRetrieveAPIView, \
    SubjectUpdateAPIView, SubjectDestroyAPIView

app_name = StudyPlatformConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('subject/create/', SubjectCreateAPIView.as_view(), name='create_subject'),
                  path('subject/list/', SubjectListAPIView.as_view(), name='subject_list'),
                  path('subject/<int:pk>/', SubjectRetrieveAPIView.as_view(), name='subject_view'),
                  path('subject/update/<int:pk>/', SubjectUpdateAPIView.as_view(), name='subject_update'),
                  path('subject/delete/<int:pk>/', SubjectDestroyAPIView.as_view(), name='subject_delete'),

              ] + router.urls
