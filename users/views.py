from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, HttpResponseRedirect
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
        owners = Owner.objects.filter(society = secretary[0])
        return render(request, 'societies/bill.html', {'flat_owners': owners, 'society': secretary[0]})
    return render(request, 'societies/message.html', 
                    {'message': 'You are not authorized for this action'})

@login_required
def sendBill(request):
    secretary = SocietyDetail.objects.filter(secretary = request.user)
    
    if secretary:
        if request.method == 'POST':
            selectedOwners = request.POST.getlist('select_user')
            society = get_object_or_404(SocietyDetail, society_name = request.POST['society'])
            description = request.POST['description']

            # loop through selected owners and save in maintenance bill
            for i in selectedOwners:
                MaintenanceBill(
                    for_owner = get_object_or_404(User, username = i),
                    society = society,
                    description = description
                    ).save()
            print('hi nitin how are you my man')
            messages.success(request, 'Bill Sent Successfully!')
            return HttpResponseRedirect('/home/')

        else:
            return render(request, 'societies/message.html', 
                    {'message': 'Oops! That is a bad request'})
                            
    return render(request, 'societies/message.html', 
                    {'message': 'You are not authorized for this action'})