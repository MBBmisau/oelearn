from django.contrib.auth.backends import ModelBackend
from oscar.core.compat import get_user_model

User = get_user_model()

class UsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        # Check the token and return a user.
        username = username
        password = password
        
        try:
           user = User.objects.get(username=username)
           
           if user.check_password(password) is True:
               return user
        except User.DoesNotExist:
            return None