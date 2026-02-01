import random
import string
from django.core.cache import cache
from django.conf import settings


def generate_otp(length=4):
    """Генерация цифрового"""
    return ''.join(random.choices(string.digits, k=length))


def send_sms(phone_number, code):

    if settings.SMS_SERVICE_MOCK:
        print(f"Mock SMS to {phone_number}: Your verification code is {code}")
        return True


def store_otp(phone_number, code, timeout=300):
    """Сохраняем в кеше"""
    cache.set(phone_number, code, timeout=timeout)


def verify_otp(phone_number, code):
    """Проверка кода"""
    cached_code = cache.get(phone_number)
    return cached_code is not None and cached_code == code


def send_sms_mock(phone_number, code):
    """функция для отправки SMS"""

    import requests
    response = requests.post(
        'https://sms-service.com/api/send',
        data={
            'api_key': settings.SMS_SERVICE_API_KEY,
            'to': phone_number,
            'message': f'Your code: {code}',
            'sender': settings.SMS_SENDER_NAME
        }
    )
    return response.status_code == 200


def get_remaining_time(phone_number):
    """Получение оставшегося времени"""
    cache_key = f"otp_{phone_number}"
    ttl = cache.ttl(cache_key)
    return max(0, ttl) if ttl else 0