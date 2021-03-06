from django.db import models

from user.models import User
from classroom.models import Classroom

class Inbox_content(models.Model):
    title = models.CharField(max_length=255, default="No title")
    content = models.TextField(default="")
    
    def __str__(self):
        return self.title

class Inbox(models.Model):
    send_datetime = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_profile')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_profile')
    content = models.ForeignKey(Inbox_content, on_delete=models.CASCADE, blank=True)
    read = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.content.title