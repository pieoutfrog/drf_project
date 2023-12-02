from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


def forbidden_url(value):
    url = urlparse(value)
    if url.netloc != 'www.youtube.com' or url.scheme != 'https':
        raise ValidationError('Ссылка на видео должна быть только из ютуба, ты чево!')
