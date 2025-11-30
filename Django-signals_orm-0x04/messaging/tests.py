from django.test import TestCase
from django.contrib.auth.models import User
from messaging.models import Message, Notification


class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="pass123")
        self.receiver = User.objects.create_user(username="receiver", password="pass123")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello there!"
        )

        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)

        notif = notifications.first()
        self.assertEqual(notif.message, msg)
        self.assertFalse(notif.is_read)

