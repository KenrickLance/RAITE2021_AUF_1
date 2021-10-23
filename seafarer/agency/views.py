from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from seafarer import settings
from .utils import send_email, generate_confirmation_token, confirm_token
from .forms import CrewCreationForm, ShipCreationForm, CharterCreationForm
import json



def test(request):
    form = CharterCreationForm()
    return render(request, 'agency/test.html', {'form':form})

def dashboard(request):
    context = {
        'page_name': 'Dashboard'
    }
    return render(request, 'agency/dashboard.html', context)


def crew_add(request):
    context = {
        'page_name': 'Crew',
        'form': CrewCreationForm()
    }
    return render(request, 'agency/crew.html', context)


@require_http_methods(['POST'])
def crew_create(request):
    form = CrewCreationForm(request.POST)
    if form.is_valid():
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})


def charters_add(request):
    context = {
        'page_name': 'Charters',
        'form': CharterCreationForm()
    }
    return render(request, 'agency/charters.html', context)


def ships_add(request):
    if request.method == 'POST':
        print('post')
    context = {
        'page_name': 'Ships',
        'form': ShipCreationForm()
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

