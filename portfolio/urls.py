from django.urls import path
  
# importing views from views..py
from .views import StockDetailView
urlpatterns = [
    # <pk> is identification for id field,
    # slug can also be used
    path('<pk>/', StockDetailView.as_view()),
]