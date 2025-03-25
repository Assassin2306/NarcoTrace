from rest_framework import serializers
from .models import FlaggedMessage

class FlaggedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlaggedMessage
        fields = ['id', 'message', 'user_id', 'chat_id', 'timestamp', 'flagged']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ensure timestamp is in ISO format
        representation['timestamp'] = instance.timestamp.isoformat()
        return representation
