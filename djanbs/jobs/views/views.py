from django.shortcuts import redirect, render

from ..models import JobOffer


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
