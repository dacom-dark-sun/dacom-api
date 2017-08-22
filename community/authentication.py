from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import authentication

from community.models import Community


class ApiKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_API_KEY', '')

        try:
            community = Community.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            request.community = None
            return None

        request.community = community

        # TODO Реализовать пользователя для сообщества
        # По дефолту вернем админа как вторизованного пользователя
        return (User.objects.get(username='admin'), None)
