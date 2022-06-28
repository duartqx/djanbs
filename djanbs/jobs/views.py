from django.shortcuts import render
from .models import JobOffer

def home(request):
    job_offers = JobOffer.objects.all() # type: ignore
    return render(request, 'jobs/base.html', {'job_offers': job_offers})
