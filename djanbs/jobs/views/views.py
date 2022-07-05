from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError
from django.shortcuts import Http404, redirect, render

from jobs.forms import (CandidateRegisterForm, CompanyRegisterForm, 
                        JobCandidateForm, JobOfferCreationForm)

from ..choices import (EducationRequirement, PaymentRange, 
                       PositionLevel, int_to_string)
from ..decorators import allowed_groups
from ..models import Candidate, Company, JobCandidated, JobOffer


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.user.is_candidate:
            job_offers = JobOffer.objects.all() # type: ignore
            context = { 'job_offers': job_offers, }
            return render(request, 'jobs/index.html', context)
        else:
            company = Company.objects.get(pk=request.user.company.id) # type: ignore
            company_offers = JobOffer.objects.filter(company=company) # type: ignore
            job_candidated = [ 
                JobCandidated.objects.filter( # type: ignore
                job_offer=offer).values('candidate').distinct().count() 
                for offer in company_offers ]
            context = { 
                'company_offers_cand': zip(company_offers,job_candidated),
                }
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
    if request.method == 'POST' and request.user.company.id == job_offer.company.id:
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
    if request.method == 'POST' and request.user.company.id == job_offer.company.id:
        job_offer.delete()
        return redirect('home')
    context = {
        'job_offer': job_offer,
        }
    return render(request, 'jobs/delete-job.html', context)


@allowed_groups(allowed_roles=['company'])
def details_job_offer(request, pk):
    job_offer = JobOffer.objects.get(id=pk) # type: ignore
    if request.user.company.id == job_offer.company.id:
        offer_cnd = [jc for jc in JobCandidated.objects.filter(job_offer=job_offer)] # type: ignore
        offer_cnd = sorted(offer_cnd,key=lambda x: x.cand_pontuation(), reverse=True)
        
        context = {
            'job_offer': job_offer,
            'offer_candidates': offer_cnd,
            }

        return render(request, 'jobs/details-job.html', context)
    raise Http404


@allowed_groups(allowed_roles=['company'])
def cand_details(request, jc_id):
    jc = JobCandidated.objects.get(id=jc_id) # type: ignore
    jc_education: tuple[str, str] = (
        int_to_string(EducationRequirement, jc.candidate.education), 
        int_to_string(EducationRequirement, jc.job_offer.education_req)
        )
    jc_position_level: tuple[str, str] = (
        int_to_string(PositionLevel, jc.candidate.position_level), 
        int_to_string(PositionLevel, jc.job_offer.position_level)
        )
    jc_payment_range: tuple[str, str]= (
        int_to_string(PaymentRange, jc.candidate.payment_range), 
        int_to_string(PaymentRange, jc.job_offer.payment_range)
        )
    context = { 
        'jc': jc,
        'jc_education': jc_education,
        'jc_position_level': jc_position_level,
        'jc_payment_range': jc_payment_range,
        }
    return render(request, 'jobs/detail-cand.html', context)


@allowed_groups(allowed_roles=['candidate'])
def candidate_to_job(request, job_id):
    job_offer = JobOffer.objects.get(pk=job_id) # type: ignore
    candidate = Candidate.objects.get(id=request.user.candidate.id) # type: ignore

    form = JobCandidateForm()
    if request.method == 'POST':
        try:
            form = JobCandidateForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.job_offer = job_offer
                obj.candidate = candidate
                obj.save()

                messages.success(request, f'Successfully applied to {job_offer}!')
                return redirect('home')
        except IntegrityError:
            messages.error(
                request, f'You\'re already applied yourself for this position!')
            return redirect('home')


    context = {
        'form':form, 
        'job_offer': job_offer,
        'candidate': candidate,
        'payment': int_to_string(PaymentRange, job_offer.payment_range),
        'education': int_to_string(EducationRequirement, job_offer.education_req),
        'pos_level': int_to_string(PositionLevel, job_offer.position_level),
    }

    return render(request, 'jobs/job-candidate.html', context)


@allowed_groups(allowed_roles=['candidate'])
def candidate_profile(request):
    candidated = JobCandidated.objects.filter(candidate=request.user.candidate) # type: ignore
    context = { 'candidated': candidated, }
    return render(request, 'jobs/candidate-profile.html', context)


def profile(request):
    if request.user.is_candidate:
        return candidate_profile(request)
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
    context = {
            'form': form,
            }
    return render(request, template, context)


def profile_edit(request):
    if request.user.is_candidate:
        return _edit_profile(request, 
                CandidateRegisterForm, 'registration/cand-register.html')
    else:
        return _edit_profile(request, 
                CompanyRegisterForm, 'registration/comp-register.html')


@allowed_groups(allowed_roles=['company'])
def company_profile(request):
    #context = {}
    #return render(request, 'jobs/company-profile.html', context)
    return profile_edit(request)


@allowed_groups(allowed_roles=['candidate'])
def delete_job_application(request, job_id):
    job_candidated = JobCandidated.objects.get(pk=job_id) # type: ignore
    if request.method == "POST":
        job_candidated.delete()
        return redirect('profile')
    context = {
        'job_candidated': job_candidated,
        }
    return render(request, 'jobs/delete-job-cand.html', context)
