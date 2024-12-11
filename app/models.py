from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    role_choices = (
        ('Manager','Manager'),
        ('Staff','Staff'),
    )
    role = models.CharField(max_length = 10, choices = role_choices, default = 'Staff')
    username = models.CharField(max_length = 255, unique = True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Roster model
class Roster(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="roster")
    working_days = models.JSONField()  # Example: {"Monday": "9 AM - 5 PM", "Tuesday": ...}
    weekly_offs = models.JSONField()  # Example: ["Saturday", "Sunday"]

# Shift model
class Shift(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name="shifts")
    day = models.JSONField(max_length=20)  
    shift_time = models.JSONField(max_length=50) 
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shifts")

# Attendance model
class Attendance(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")
    timestamp = models.DateTimeField(default=now)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='attendance_images/')