from django.db import models

# Create your models here.

class Market(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    net_worth = models.DecimalField(max_digits=100, decimal_places=2)
    
    def __str__(self):
        return self.name