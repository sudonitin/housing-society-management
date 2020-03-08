from django.shortcuts import render, redirect, get_list_or_404
from .forms import RegisterUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User

from societies.models import SocietyDetail, Owner, Forum, MaintenanceBill

def landing(request):
    return render(request, 'users/land.html')

@login_required
def home(request):
    loggedinUser = Owner.objects.filter(name = request.user)
    secretary = SocietyDetail.objects.filter(society_name = loggedinUser[0].society)
    flatOwners = Owner.objects.filter(society = secretary[0])
    isSec = (str(request.user) == str(secretary[0].secretary))
    return render(
            request, 
            'users/home.html', 
            {
            'secretary': secretary[0], 
            'flatOwners': flatOwners, 
            'isSec': isSec
            }
        ) 

@login_required
def createBill(request):
    secretary = SocietyDetail.objects.filter(secretary = request.user)
    if secretary:
        return render(request, 'societies/bill.html')
    return render(request, 'societies/message.html', 
                    {'message': 'You are not authorized for this action'})