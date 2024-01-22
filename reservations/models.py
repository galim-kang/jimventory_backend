from django.db import models
from django.conf import settings

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    storage = models.ForeignKey('storages.Storage', on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True, auto_now=True)
    bag_count = models.PositiveIntegerField(default=1)  
    notes = models.TextField(blank=True, null=True) 
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')), default='pending')

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]
    def __str__(self):
        return f"{self.user.username}'s reservation at {self.storage.serviceName}"
