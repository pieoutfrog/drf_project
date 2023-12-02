from rest_framework import serializers

from study_platform.models import Course, Subject, Payment


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lesson = SubjectSerializer(source='lessons', many=True, read_only=True)

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
