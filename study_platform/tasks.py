import logging
import smtplib

from celery import shared_task
from django.core.mail import send_mail
from study_platform.models import Subscription
from config import settings


logger = logging.getLogger(__name__)


@shared_task
def send_mail_about_updates(course_id):
    object_subs = Subscription.objects.filter(course=course_id)
    for sub in object_subs:
        try:
            send_mail(
                subject=f'Курс {sub.course.title} был обновлен',
                message=f'Курс {sub.course.title} был обновлен, проверь, чтобы не пропустить ничего интересного!)',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[sub.user.email],
                fail_silently=False,
            )

            logger.info(f'Сообщение направлено {sub.user.email}')
        except smtplib.SMTPException as e:
            print(f'Ошибка при отправке письма: {str(e)}')