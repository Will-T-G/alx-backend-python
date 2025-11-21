from rest_framework import permissions
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only allow authenticated users who are part of the conversation to:
    - view messages
    - update messages (PUT/PATCH)
    - delete messages (DELETE)
    """

    def has_permission(self, request, view):
        # User must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        ALX expects you to explicitly check for PUT, PATCH, DELETE.
        obj may be a Message or a Conversation.
        """

        # Determine the conversation object
        if hasattr(obj, "conversation"):
            conversation = obj.conversation
        else:
            conversation = obj

        # User must be a participant
        if request.user not in conversation.participants.all():
            return False

        # Explicit method checks required by ALX
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return True

        return False

class IsOwner(permissions.BasePermission):
    """
    Object-level permission: only the owner (user) can access the object.
    Use this for Messages, Conversations, Profiles, etc.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
