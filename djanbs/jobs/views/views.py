from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from jobs.forms import CandidactRegisterForm, CompanyRegisterForm, JobCandidactForm, JobOfferCreationForm

from ..models import Candidact, Company, JobCandidacted, JobOffer
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
    form = JobOfferCreationForm()
    if request.method == 'POST':
        form = JobOfferCreationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = company
            obj.save()
            return redirect('home')
    context = {
        'form': form, 
        'operation': 'Create',
        }
    return render(request, 'jobs/create-job.html', context)



@allowed_groups(allowed_roles=['company'])
def edit_job_offer(request, pk):
    job_offer = JobOffer.objects.get(id=pk) # type: ignore
    form = JobOfferCreationForm(instance=job_offer)
    if request.method == 'POST':
        form = JobOfferCreationForm(request.POST, instance=job_offer)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form, 
        'operation': 'Edit',
        }
    return render(request, 'jobs/create-job.html', context)


@allowed_groups(allowed_roles=['company'])
def delete_job_offer(request, pk):
    job_offer = JobOffer.objects.get(id=pk) # type: ignore
    if request.method == 'POST':
        job_offer.delete()
        return redirect('home')
    context = {
        'job_offer': job_offer,
        }
    return render(request, 'jobs/delete-job.html', context)


@allowed_groups(allowed_roles=['candidact'])
def candidact_to_job(request, job_id):
    job_offer = JobOffer.objects.get(pk=job_id) # type: ignore
    candidact = Candidact.objects.get(id=request.user.candidact.id) # type: ignore

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


def candidact_profile(request):
    candidacted = JobCandidacted.objects.filter(candidact=request.user.candidact) # type: ignore
    context = { 'candidacted': candidacted, }
    return render(request, 'jobs/candidact_profile.html', context)


def company_profile(request):
    context = {}
    return render(request, 'jobs/company_profile.html', context)


def profile(request):
    if request.user.groups.all()[0] == 'candidact':
        return candidact_profile(request)
    else:
        return company_profile(request)


def _edit_profile(request, form_model, template):
    user = request.user
    form = form_model(instance=user)
    if request.method == 'POST':
        form = form_model(request.POST, instance=user)
        if form.is_valid():
            form.save(create=False)
            login(request, user)
            messages.success(request, 'Successfully updated your profile')
            return redirect('profile')
    context = {'form': form}
    return render(request, template, context)


def profile_edit(request):
    if request.user.groups.filter(name='candidact').exists():
        return _edit_profile(request, 
                CandidactRegisterForm, 'registration/cand-register.html')
    else:
        return _edit_profile(request, 
                CompanyRegisterForm, 'registration/comp-register.html')


def delete_job_application(request, job_id):
    job_candidacted = JobCandidacted.objects.get(pk=job_id) # type: ignore
    if request.method == "POST":
        job_candidacted.delete()
        return redirect('profile')
    context = {
        'job_candidacted': job_candidacted,
        }
    return render(request, 'jobs/delete-job-cand.html', context)
