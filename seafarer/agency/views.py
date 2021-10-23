from django.shortcuts import render, get_object_or_404
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
    }
    if request.method == 'POST':
        form = CrewCreationForm(request.POST)
        if form.is_valid():
            new_crew = form.save()
            return HttpResponseRedirect(reverse('agency:crew_add'))
    else:
        form = CrewCreationForm()
    context['form'] = form
    return render(request, 'agency/crew_add.html', context)

def crew_manage(request):
    context = {
        'page_name': 'Crew',
    }
    crews = Crew.objects.all()
    context['crews'] = crews
    return render(request, 'agency/crew_manage.html', context)

def crew_manage_one(request, pk):
    context = {
        'page_name': 'Crew',
    }
    crew = get_object_or_404(Crew, pk=pk)
    form = CrewCreationForm(instance=crew)
    context['form'] = form
    return render(request, 'agency/crew_manage_one.html', context)

@require_http_methods(['POST'])
def crew_edit(request, pk):
    context = {
        'page_name': 'Crew',
    }
    form = CrewCreationForm(request.POST)
    if form.is_valid():
        new_crew = form.save()
        return HttpResponseRedirect(reverse('agency:crew_manage'))
    else:
        context['form'] = form
        return render(request, 'agency/crew_manage.html', context)

def charters_delete(request, pk):
    context = {

        'page_name': 'Charters',
        'form': CharterCreationForm()
    }
    crew = get_object_or_404(Crew, pk=pk)
    context['crew'] = crew
    return render(request, 'agency/crew_delete.html', context)

@require_http_methods(['POST'])
def charter_create(request):
    form = CharterCreationForm(request.POST)
    if form.is_valid():
        new_charter = form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'errors': form.errors})

def ships_add(request):
    if request.method == 'POST':
        print('post')
    context = {
        'page_name': 'Ships',
        'form': ShipCreationForm()
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

