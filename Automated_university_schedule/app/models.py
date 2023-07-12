from django.db import models

class Run(models.Model):
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    updated_screenshots = models.IntegerField(default=0)
    last_status = models.CharField(max_length=60)
