from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Ticket(models.Model):
    title = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150)
    user_filed = models.CharField(max_length=50)
    user_assigned = models.CharField(max_length=50, null=True)
    user_completed = models.CharField(max_length=50, null=True)
    ticket_status_choices = [("New", "New"), ("In_Progress", "In_Progress"),
                             ("Done", "Done"), ("Invalid", "Invalid")]
    ticket_status = models.CharField(
        max_length=15, default="New", choices=ticket_status_choices)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
