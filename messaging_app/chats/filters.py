import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages sent after this datetime
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )

    # Filter messages sent before this datetime
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    # Filter messages from a specific user
    user_id = django_filters.NumberFilter(
        field_name="user__id", lookup_expr="exact"
    )

    class Meta:
        model = Message
        fields = ["user_id", "created_after", "created_before"]
