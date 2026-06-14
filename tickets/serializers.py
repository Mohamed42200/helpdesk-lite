from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer

from .models import Comment, Ticket


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'message', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.AGENT),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'priority', 'status',
            'created_by', 'assigned_to', 'assigned_to_id',
            'created_at', 'updated_at', 'comments',
        ]
        read_only_fields = [
            'id', 'created_by', 'status', 'created_at', 'updated_at', 'comments',
        ]


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status', 'assigned_to']

    def validate_status(self, value):
        valid = [c[0] for c in Ticket.Status.choices]
        if value not in valid:
            raise serializers.ValidationError('Invalid status.')
        return value

    def validate_assigned_to(self, value):
        if value and not value.is_agent():
            raise serializers.ValidationError('Can only assign to agents.')
        return value


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message']
