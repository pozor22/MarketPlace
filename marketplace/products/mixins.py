from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class NotAuthenticatedRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class SellerRequiredMixin:

    group_name = "seller"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.group_name:
            try:
                group = Group.objects.get(name=self.group_name)
                if group not in request.user.groups.all():
                    return self.handle_no_permission()
            except Group.DoesNotExist:
                return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        """
        Метод для обработки случая, когда у пользователя нет доступа.
        Можно переопределить в дочерних классах.
        """
        raise PermissionDenied("У вас нет прав для доступа к этой странице.")
