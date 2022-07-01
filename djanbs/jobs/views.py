from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .decorators import unauthenticated_user
from .models import JobOffer


def home(request):
    job_offers = JobOffer.objects.all() # type: ignore
    user_name = request.user if request.user.id is not None else ''
    in_or_out = 'logout' if user_name != '' else 'login'
    print(user_name, in_or_out)
    context = {
        'job_offers': job_offers,
        'user_name': user_name,
        'in_or_out': in_or_out,
    }
    if user_name == '':
        return redirect('login')
    else:
        return render(request, 'jobs/index.html', context)


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            print('user login')
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user}')
            return redirect('login')
            # redirect to choose type of account

    return render(request, 'register.html', {'form': form})

# request.user clica no botão que já tem a job_offer marcada e já faz o post ali
# request.user.id - job_offer.id
