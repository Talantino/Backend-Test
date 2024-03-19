from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def subscription(request):
    if request.user.group:
        return Subscription.objects.filter(
            student=request.user,
            course=request.user.group.course
        ).exists()
    return False


class IsStudentOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or (
            request.method in SAFE_METHODS
            and request.user.is_authenticated
            and subscription(request)
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (
            request.method in SAFE_METHODS
            and request.user.is_authenticated
            and subscription(request)
        )


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
