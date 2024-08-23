from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Diagn(models.Model):
    gpu_t = models.IntegerField()
    gpu_load = models.IntegerField()
    processor_t = models.IntegerField()
    processor_load = models.IntegerField()
    memori_load = models.IntegerField()
    disk_load = models.IntegerField()
    proces_load = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    terminal_name = models.CharField(max_length=200)
