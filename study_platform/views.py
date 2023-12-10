import stripe
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from study_platform.tasks import send_mail_about_updates
from config.settings import STRIPE_API_KEY
from study_platform.models import Course, Subject, Payment, Subscription
from study_platform.paginators import SubjectPaginator, CoursePaginator
from study_platform.permissions import IsOwner, IsModer
from study_platform.serializers import CourseSerializer, SubjectSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentSuccessSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ Отображает список курсов, создает, обновляет курсы """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def perform_update(self, serializer):
        updated_course = serializer.save()
        updated_course.owner = self.request.user
        updated_course.save()

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsModer]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModer]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class SubjectCreateAPIView(generics.CreateAPIView):
    """ Создает предмет """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        send_mail_about_updates.delay(new_lesson.course.id)
        new_lesson.save()


class SubjectListAPIView(generics.ListAPIView):
    """ Отображает список предметов """
    serializer_class = SubjectSerializer
    pagination_class = SubjectPaginator
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class SubjectRetrieveAPIView(generics.RetrieveAPIView):
    """ Отображает один предмет """
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubjectUpdateAPIView(generics.UpdateAPIView):
    """ Обновляет предмет """
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        updated_lesson = serializer.save()
        updated_lesson.owner = self.request.user
        send_mail_about_updates.delay(updated_lesson.course.id)
        updated_lesson.save()


class SubjectDestroyAPIView(generics.DestroyAPIView):
    """ Удаляет предмет """
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    """ Отображает список оплат """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создает оплату """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Отображает одну оплату """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionListAPIView(generics.ListAPIView):
    """ Отображает список подписок """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Создает подписку """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """ Удаляет подписку """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentSuccessAPIView(generics.RetrieveAPIView):
    """ Успешная оплата """
    stripe.api_key = STRIPE_API_KEY
    serializer_class = PaymentSuccessSerializer
    queryset = Payment.objects.all()

    def get_object(self):

        session_id = self.request.query_params.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)

        payment_id = session.metadata['payment_id']
        obj = get_object_or_404(self.get_queryset(), pk=payment_id)

        if not obj.is_paid:
            if session.payment_status == 'paid':
                obj.is_paid = True
                obj.save()
        return obj
