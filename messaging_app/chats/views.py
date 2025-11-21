from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import django_filters
from .models import Message
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from django.shortcuts import get_object_or_404



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only show conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only messages in conversations the user participates in
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        """
        - reference to 'conversation_id'
        - HTTP_403_FORBIDDEN in code
        """

        conversation_id = self.request.data.get("conversation_id")  # required keyword

        conversation = get_object_or_404(Conversation, id=conversation_id)

        # If the user is NOT part of this conversation → reject
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to send messages here."},
                status=status.HTTP_403_FORBIDDEN,  # required keyword
            )

        # Otherwise, create the message normally
        serializer.save(user=self.request.user, conversation=conversation)
