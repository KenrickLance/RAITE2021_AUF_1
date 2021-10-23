from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from seafarer import settings
from .utils import send_email, generate_confirmation_token, confirm_token
from .models import Crew, Ship, Charter
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


@require_http_methods(['GET', 'POST'])
def crew_create(request):
    if request.method == 'POST':
        form = CrewCreationForm(request.POST)
        if form.is_valid():
            new_crew = form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'errors': form.errors})
    else:
        form = CrewCreationForm()
        return form
@require_http_methods(['GET', 'PUT'])
def crew_edit(request):
    form = CrewCreationForm(request.POST)
    if form.is_valid():
        new_crew = form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})

@require_http_methods(['PUT'])
def crew_edit(request):
    form = CrewCreationForm(request.POST)
    if form.is_valid():
        new_crew = form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})


def charters_add(request):
    context = {
        'page_name': 'Charters'
    }
    return render(request, 'agency/charters.html', context)

@require_http_methods(['POST'])
def charter_create(request):
    form = CharterCreationForm(request.POST)
    if form.is_valid():
        new_charter = form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})

def ships(request):
    context = {
        'page_name': 'Ships'
    }
    return render(request, 'agency/ships.html', context)

@require_http_methods(['POST'])
def ship_create(request):
    form = ShipCreationForm(request.POST)
    if form.is_valid():
        new_ship = form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})

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

