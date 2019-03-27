from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORIES = (
    ("traffic", "TRAFFIC"),
    ("conversion_rate", "CONVERSION RATE"),
    ("marketing", "MARKETING"),

)


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_completed = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=255, choices=CATEGORIES, default="traffic")
    done_message = models.TextField(null=True, default="")
    video_url = models.CharField(max_length=255, default="")
    task_can_be_repeated = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    user_completed = models.BooleanField(default=False)
    content = models.TextField(blank=True, default="")
    order = models.IntegerField(default=0)
    step_number = models.IntegerField(default=1)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=255, default="")

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.title
