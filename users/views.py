from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, HttpResponseRedirect
from .forms import RegisterUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import JsonResponse

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

@login_required
def pendingBills(request):
    pending = MaintenanceBill.objects.filter(for_owner = request.user, paid = 'no')
    return render(request, 'societies/pendingBill.html', {'bills': pending})

# forum for respective society
@login_required
def forumDisplay(request):
    owner = get_object_or_404(Owner, name = request.user)
    issues = Forum.objects.filter(society = owner.society)
    voters = [issue.voters.strip('][').split(', ') for issue in issues]
    # voters = [voter.strip("'") for voter in voters[0]]
    return render(request, 'societies/forumPage.html', 
                {
                'issues': issues, 
                'society_name': owner.society,
                'voters': voters,
                }
    )

@login_required
def upVote(request):
    print('hello', request.GET['issueId'])
    issueId = get_object_or_404(Forum, pk = request.GET['issueId'])
    voters = issueId.voters.strip('][').split(', ')
    if '' in voters:
        voters.remove('')
    voters = [i.strip("'") for i in voters]
    voters.append(str(request.user))
    issueId.voters = str(voters)
    issueId.votes = len(voters)
    issueId.save()
    forumDisplay(request)
    data = {'message': 'upvoted successfully', 'upvoted': True}
    return JsonResponse(data)

@login_required
def newTopic(request):
    if request.method == 'POST':
        owner = get_object_or_404(Owner, name = request.user)
        Forum(title = request.POST['title'], description = request.POST['description'],
                creator = request.user, society = owner.society).save()
        messages.success(request, 'Topic created successfully!')
        return HttpResponseRedirect('/forum/')
    else:
        return render(request, 'societies/newTopic.html')