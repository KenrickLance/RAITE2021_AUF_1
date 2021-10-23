from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from seafarer import settings
from .utils import send_email, generate_confirmation_token, confirm_token
from .forms import CrewCreationForm, ShipCreationForm, CharterCreationForm

def test(request):
    form = CharterCreationForm()
    return render(request, 'agency/test.html', {'form':form})

def dashboard(request):
    context = {
        'page_name': 'Dashboard'
    }
    return render(request, 'agency/dashboard.html', context)

def crew(request):
    context = {
        'page_name': 'Crew',
        'form': CrewCreationForm()
    }
    return render(request, 'agency/crew.html', context)

@require_http_methods(['POST'])
def crewCreate(request):
    form = CrewCreationForm(request.POST)
    if form.is_valid():
        return HttpResponseRedirect(reverse('polls:results'))

def charters(request):
    context = {
        'page_name': 'Charters'
    }
    return render(request, 'agency/charters.html', context)

def ships(request):
    context = {
        'page_name': 'Ships'
    }
    return render(request, 'agency/ships.html', context)

def analytics(request):
    context = {
        'page_name': 'Analytics'
    }
    return render(request, 'agency/analytics.html', context)

def apply(request):
    context = {
        'page_name': 'Apply'
    }
    return render(request, 'agency/apply.html', context)

