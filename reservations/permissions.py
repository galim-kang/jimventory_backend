# reservations/permissions.py

from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    객체의 소유자 또는 관리자만 요청을 허용합니다.
    """

    def has_object_permission(self, request, view, obj):
        # 관리자의 경우 모든 요청을 허용
        if request.user.is_staff:
            return True
        # 소유자인 경우에만 요청을 허용
        return obj.user == request.user
