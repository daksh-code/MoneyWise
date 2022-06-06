from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from stockproject import settings
from mainapp.models import UserPortfolio
from datetime import date

@shared_task(bind=True)
def send_mail_func(self):
    
    lockinends=UserPortfolio.objects.all()
    

    #dateportfolio=UserPortfolio.objects.filter(date=date.today())
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for i in lockinends:
        mail_subject = f"MoneyWise lockin period ends for {i.stockname} for {i.quantity} quantity"
        message = "You can now release your stocks"
        user=i.owner
        to_email = user.email
        print(user)
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )
    return "Done"

@shared_task(bind=True)
def send_mail_func_portfolio(self):
    #timezone.localtime(users.date_time) + timedelta(days=2)
    dateportfolio=UserPortfolio.objects.filter(date=date.today())
    temp={}
    print(dateportfolio)
    for i in dateportfolio:
        if(temp.get(i.owner)!=None):
            continue
        else:
            temp[i.owner]=1
            mail_subject = "MoneyWise Your Portfolio"
            message = "Link to your portfolio ..."
            user=i.owner
            to_email = user.email
            send_mail(
                subject = mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False,
            )
    return "Done"