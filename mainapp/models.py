from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StockDetail(models.Model):
    stock = models.CharField(max_length=255, unique=True)
    user = models.ManyToManyField(User)

from django.utils.timezone import now
# Create your models here.

class UserPortfolio(models.Model):
    price = models.FloatField()
    quantity=models.IntegerField()
    date = models.DateField(default=now)
    lockindate =models.DateField(blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stockname = models.CharField(max_length=266)
    
    def __str__(self):
        return self.stockname

    class Meta:
        ordering: ['-date']