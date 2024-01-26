# from accounts.models import Man
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
           return Man.objects.get(pk=user_id)
        except Man.DoesNotExist:
           return None

    def authenticate(self, request, username, password):

        try:
            user = Man.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )

        except Man.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        else:
            return None