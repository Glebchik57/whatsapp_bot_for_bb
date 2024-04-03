from django.db import models


class Reminder(models.Model):
    author = models.CharField(max_length=30)
    text = models.CharField(max_length=200)
    time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'time'],
                name='unique_reminder'
            )
        ]
