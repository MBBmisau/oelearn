from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class UserProductMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user in self.product.users.all() and self.product.live