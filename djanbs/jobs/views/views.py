from django.contrib import messages
from django.shortcuts import redirect, render

from jobs.forms import JobCandidactForm, JobOfferCreationForm

from ..models import Candidact, Company, JobOffer
from ..choices import EducationRequirement, PaymentRange, PositionLevel, int_to_string
from ..decorators import allowed_groups


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.user.groups.filter(name='candidact').exists():
            job_offers = JobOffer.objects.all() # type: ignore
            context = { 'job_offers': job_offers, }
            return render(request, 'jobs/index.html', context)
        else:
            company = Company.objects.get(pk=request.user.company.id) # type: ignore
            company_offers = JobOffer.objects.filter(company=company) # type: ignore
            context = { 'company_offers': company_offers, }
            return render(request, 'jobs/company.html', context)


@allowed_groups(allowed_roles=['company'])
def create_job_offer(request, pk):
    company = Company.objects.get(id=pk) # type: ignore
    #form = JobOfferCreationForm(initial={'company':company})
    form = JobOfferCreationForm()
    if request.method == 'POST':
        form = JobOfferCreationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = company
            obj.save()

            return redirect('home')
    return render(request, 'jobs/create-job.html', {'form': form, 'company': company})



@allowed_groups(allowed_roles=['company'])
def edit_job_offer(request, pk):
    job_offer = JobOffer.objects.get(pk=pk) # type: ignore
    form = JobOfferCreationForm(instance=job_offer)
    if request.method == 'POST':
        pass



@allowed_groups(allowed_roles=['candidact'])
def candidact_to_job(request, job_id):
    job_offer = JobOffer.objects.get(pk=job_id) # type: ignore
    candidact = Candidact.objects.get(user_id=request.user) # type: ignore

    form = JobCandidactForm()
    if request.method == 'POST':
        form = JobCandidactForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.job_offer = job_offer
            obj.candidact = candidact
            obj.save()

            messages.success(request, f'Successfully candidacted to {job_offer}!')
            return redirect('home')

    context = {
        'form':form, 
        'job_offer': job_offer,
        'candidact': candidact,
        'payment': int_to_string(PaymentRange, job_offer.payment_range),
        'education': int_to_string(EducationRequirement, job_offer.education_req),
        'pos_level': int_to_string(PositionLevel, job_offer.position_level),
    }

    return render(request, 'jobs/job-candidact.html', context)
