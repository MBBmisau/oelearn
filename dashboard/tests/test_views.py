from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from custom_auth.models import CustomUser

class DashboardAdminTestCase(TestCase):
    ADMIN_EMAIL = 'mbb@gmail.com'
    ADMIN_PASSWORD = 'Test12345'

    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(first_name='Muhammad', email=self.ADMIN_EMAIL, 
            reg_id='1000', user_type=CustomUser.STUDENT,password=self.ADMIN_PASSWORD)

class DashboardAdminOrInstructorTestCase(DashboardAdminTestCase):
    pass