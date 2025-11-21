from rest_framework import permissions
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only if:
    - user is authenticated
    - user is a participant in the conversation of the object
    """

    def has_permission(self, request, view):
        # User must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be:
        - a Conversation instance (with participants ManyToMany)
        - a Message instance (with message.conversation)
        """
        # Case 1: obj *is* a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Case 2: obj *is* a Message that belongs to a conversation
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False


class IsOwner(permissions.BasePermission):
    """
    Object-level permission: only the owner (user) can access the object.
    Use this for Messages, Conversations, Profiles, etc.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
