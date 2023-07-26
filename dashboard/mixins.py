from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from custom_auth.models import CustomUser

class AdminOrTeacherMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin or self.request.user.user_type == CustomUser.TEACHER

class AdminOrInstructorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin or self.request.user == self.course.instructor.user
