from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.stockPicker,name='stockpicker'),
    path('stocktracker/',views.stockTracker,name='stocktracker'),
    path('stockdetail/',views.stockDetail,name='stockdetail'),
    path('portfoliosummary/',views.stockPortfolios,name='portfoliosummary'),
    path('portfolio/',views.portfolio_view,name='stockportfolio'),
    path('deletestock/<str:id>', views.delete_stock, name='deletestock'),
    path('sendmail/',views.send_mail_to_all,name='sendmail'),
    path('schedulemail/', views.schedule_mail, name="schedulemail"),
    
    


]