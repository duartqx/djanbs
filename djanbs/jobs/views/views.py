from django.shortcuts import redirect, render

from jobs.forms import JobOfferCreationForm

from ..models import Company, JobOffer


def home(request):
    job_offers = JobOffer.objects.all() # type: ignore
    user_name = request.user if request.user.id is not None else ''
    context = {
        'job_offers': job_offers,
        'user_name': user_name,
    }
    if user_name == '':
        return redirect('login')
    else:
        return render(request, 'jobs/index.html', context)


def create_job_offer(request, pk):
    company = Company.objects.get(id=pk) # type: ignore
    #form = JobOfferCreationForm(initial={'company':company})
    form = JobOfferCreationForm()
    if request.method == 'POST':
        #form = JobOfferCreationForm(request.POST, request.user)
        form = JobOfferCreationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = company
            obj.save()

            return redirect('home')
    return render(request, 'jobs/create-job.html', {'form': form, 'company': company})
