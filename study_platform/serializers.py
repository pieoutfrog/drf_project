from rest_framework import serializers

from study_platform.services import get_link
from study_platform.validators import forbidden_url
from study_platform.models import Course, Subject, Payment, Subscription


class SubjectSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[forbidden_url])

    class Meta:
        model = Subject
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lesson = SubjectSerializer(source='lessons', many=True, read_only=True)
    is_subscribed = SubscriptionSerializer(source='subs', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_num_lessons(instance):
        return instance.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payment_link = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    @staticmethod
    def get_payment_link(instance):
        return get_link(instance)


class PaymentSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'is_paid']