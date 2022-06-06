from django.contrib import admin
from .models import UserPortfolio
# Register your models here.
from .models import StockDetail

admin.site.register(StockDetail)
admin.site.register(UserPortfolio)