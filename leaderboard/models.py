from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.
class Player(models.Model):
    # id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, blank=False)
    flag = models.CharField(max_length=16, blank=False)
    url = models.URLField(default="",max_length=200)
    complete = models.BooleanField(default=False, blank=False)
    complete_time = models.DateTimeField(default=timezone.now, blank=False)
    def __str__(self):
        return self.username