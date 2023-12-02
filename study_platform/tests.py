from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study_platform.models import Course, Subject, Subscription
from study_platform.serializers import SubscriptionSerializer
from users.models import User


class LessonListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test',
            description='Test description'
        )
        self.lesson = Subject.objects.create(
            title='Test',
            description='Test description',
            course=self.course,
            owner=self.user
        )

    def test_get_list(self):
        """Test for getting list of lessons"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('course:lesson_list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "video_url": self.lesson.video_url,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "picture": self.lesson.picture,
                        "course": self.lesson.course_id,
                        "owner": self.lesson.owner_id
                    }
                ]
            }
        )


class LessonCreateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title="Course test"
        )

    def test_lesson_create(self):
        """ Test of lesson creation. """

        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Lesson test 2',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com'
        }

        response = self.client.post(
            reverse('course:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": response.json()["id"],
                "video_url": 'https://www.youtube.com',
                "description": None,
                "title": 'Lesson test 2',
                "picture": None,
                "course": self.course.id,
                "owner": 1
            }
        )

    def test_lesson_create_error(self):
        """ Test of forbidden lesson creation """

        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Lesson test 2',
            'course': self.course.id,
            'video_url': 'https://video-platform.com/video123'
        }

        response = self.client.post(
            reverse('course:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'video_url': ['The link from the lesson should be from YouTube!']}
        )


class LessonUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test'
        )
        self.lesson = Subject.objects.create(
            title='Test',
            description='Test description',
            video_url='https://www.youtube.com/watch',
            course=self.course,
            owner=self.user
        )

    def test_lesson_update(self):
        """Test lesson update """
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Updated lesson',
            'description': 'Updated description',
            'video_url': 'https://www.youtube.com/watch13'
        }

        response = self.client.patch(
            reverse('course:lesson_update',
                    args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated lesson')
        self.assertEqual(self.lesson.description, 'Updated description')
        self.assertEqual(self.lesson.video_url, 'https://www.youtube.com/watch13')

    def test_lesson_update_error(self):
        """Test of forbidden lesson edit"""
        self.client.force_authenticate(user=self.user)

        data = {
            'video_url': 'https://www.youhub.com/watch'
        }

        response = self.client.patch(
            reverse('course:lesson_update',
                    args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {
                             'video_url': ['The link from the lesson should be from YouTube!']
                         }
                         )


class LessonRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test'
        )
        self.lesson = Subject.objects.create(
            title='Test',
            description='Test description',
            video_url='https://www.youtube.com/watch',
            course=self.course,
            owner=self.user
        )

    def test_lesson_retrieve(self):
        """Test retrieve a lesson"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('course:lesson_detail',
                    args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LessonDestroyTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test'
        )
        self.lesson = Subject.objects.create(
            title='Test',
            description='Test description',
            video_url='https://www.youtube.com/watch',
            course=self.course,
            owner=self.user
        )

    def test_lesson_delete(self):
        """Test of lesson delete"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('course:lesson_delete',
                    args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subject.objects.filter(id=self.lesson.id).exists())

    def test_lesson_delete_outsider(self):
        """Test lesson delete if user is not owner """
        user = User.objects.create(email='outsider@outsider.com', password='outsider')
        self.client.force_authenticate(user=user)

        response = self.client.delete(
            reverse('course:lesson_delete',
                    args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test'
        )

    def test_subscription_create(self):
        """Test subscription creation"""
        self.client.force_authenticate(user=self.user)

        data = {
            'user': self.user.id,
            'course': self.course.id,
            'subscription': True
        }

        response = self.client.post(
            reverse('course:subscription_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        subscription = Subscription.objects.get()
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        self.assertEqual(subscription.subscription, True)

    def test_subscription_list(self):
        """ Test subscription list"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('course:subscription_list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscriptions = Subscription.objects.filter(user=self.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_subscription_delete(self):
        """Test deleting subscription"""
        self.client.force_authenticate(user=self.user)

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            subscription=True
        )

        response = self.client.delete(
            reverse('course:subscription_delete',
                    args=[self.subscription.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)
