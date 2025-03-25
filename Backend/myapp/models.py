# Create your models here.
from django.db import models

class FlaggedMessage(models.Model):
    message = models.TextField()
    user_id = models.CharField(max_length=100, default='unknown')
    chat_id = models.CharField(max_length=100, default='unknown')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    flagged = models.BooleanField(default=False)
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('error', 'Error')
        ],
        default='pending'
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.user_id} at {self.timestamp} - {'Flagged' if self.flagged else 'Safe'}"
