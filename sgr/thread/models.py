from django.db import models

class Thread(models.Model):
    title = models.CharField(max_length = 25)