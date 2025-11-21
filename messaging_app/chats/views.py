from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    # ALX-required filtering
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    # Pagination
    pagination_class = MessagePagination

    def get_queryset(self):
        # Users only see messages from conversations they participate in
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "Not allowed to send messages here."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save(user=self.request.user, conversation=conversation)
