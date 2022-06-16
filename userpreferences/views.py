from .models import UserPreference
from email import message
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.
def UserProfile(request):
    if request.method=='GET':
        return render(request, 'mainapp/userprofile.html')
    if request.method=='POST':
        brokerageusername=request.POST['brokerageusername']
        brokeragepassword=request.POST['brokeragepassword']
        brokerageuserdob=request.POST['brokerageuserdob']
        UserPreference.objects.filter(user=request.user).delete()
        UserPreference.objects.get_or_create(user=request.user,brokerageusername=brokerageusername,brokeragepassword=brokeragepassword,brokerageuserdob=brokerageuserdob)
        messages.success(request, 'user data saved')
        return redirect('userprofile')