from django.db import models

from facilities.models import Room, Facilities

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=50, default="")
    start_time = models.TimeField(default="")
    end_time = models.TimeField(default="")
    
class Booking(models.Model):
    book_date = models.DateField(auto_now=True)
    start_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='start_lesson_profile')
    end_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='end_lesson_profile')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)