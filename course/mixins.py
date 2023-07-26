from django.core.exceptions import PermissionDenied

class StudentCourseMixin:

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.student in self.course.students.all() or not self.course.live:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
