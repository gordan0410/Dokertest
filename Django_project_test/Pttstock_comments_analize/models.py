from django.db import models
from django.utils import timezone
# Create your models here.


class Ptt_stock_comments(models.Model):
    date = models.DateField(blank=True, null=True)
    comment = models.CharField(blank=True, max_length=70)
    created_at = models.DateTimeField(default=timezone.now)
