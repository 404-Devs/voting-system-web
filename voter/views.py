from django.shortcuts import render
from django.http import HttpResponse
from .forms import VoterRegistrationForm
from api.models import Voter

# Create your views here.

def index(request):
    return render(request, 'voter/index.html')

def registration(request):
    return render(request, 'voter/registration.html')

def addVoter(request):
    submitted = False
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("You have been registered")
    else:
        form = VoterRegistrationForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'voter/voter_registration.html', {'form': form, 'submitted': submitted})