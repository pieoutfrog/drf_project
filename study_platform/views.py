from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter

from study_platform.models import Course, Subject, Payment
from study_platform.serializers import CourseSerializer, SubjectSerializer, PaymentSerializer


class ListAPIView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class SubjectCreateAPIView(generics.CreateAPIView):
    serializer_class = SubjectSerializer


class SubjectListAPIView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectDestroyAPIView(generics.DestroyAPIView):
    queryset = Subject.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
