from django.contrib.auth.backends import ModelBackend
from pycash.models import AuthToken, TokenUsage
from django.conf import settings
from django.contrib.auth.models import User

class RemoteTokenBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteTokenMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.
    """

    def authenticate(self, remote_token, remote_user, remote_ip):
        
        if not remote_token or not remote_user:
            return

        user = None
        try:
            authtoken = AuthToken.objects.get(token=remote_token, user__username=remote_user)
            user = authtoken.user

            obj, created = TokenUsage.objects.get_or_create(token=authtoken, ip=remote_ip)
            if not created:
                obj.save() # if the object already exists, we force a save to update the last access date
        except AuthToken.DoesNotExist:
            pass
        return user

class SettingsAuthBackend:
    
    supports_anonymous_user = False
    
    def authenticate(self, username=None, password=None):
        if (username == getattr(settings,'ADMIN_LOGIN','admin') 
            and password ==  getattr(settings,'ADMIN_PWD','admin')):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username,
                                           is_staff=True,
                                           is_superuser=True)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    def has_perm(self, user_obj, perm):
        return (user_obj==getattr(settings,'ADMIN_LOGIN','admin'))
