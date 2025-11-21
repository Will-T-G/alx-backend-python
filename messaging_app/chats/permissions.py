from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission: only the owner (user) can access the object.
    Use this for Messages, Conversations, Profiles, etc.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
