from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    brokerageusername=models.CharField(max_length=266)
    brokeragepassword=models.CharField(max_length=266)
    brokerageuserdob=models.DateField(blank=True, null=True)
    
    def __str__(self):
        return str(self.user)+'s' + 'preferences'

        
