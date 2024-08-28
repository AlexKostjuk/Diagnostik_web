from django.contrib.auth.models import User
from django.db import models
from datetime import date, time
import datetime
from django.utils import timezone


# Create your models here.
class Diagn(models.Model):
    gpu_t = models.IntegerField()
    processor_t = models.IntegerField()
    processor_load = models.IntegerField()
    memori_load = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    terminal_name = models.CharField(max_length=200)
    date_comit = models.DateField(default=timezone.now)
    time_comit = models.TimeField(default=timezone.now)
