from ..forms import CandidateRegisterForm, CompanyRegisterForm
from ..models import User

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView


class CandidateRegisterView(CreateView):
    model = User
    form_class = CandidateRegisterForm
    template_name = "registration/cand-register.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "candidate"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        msg = f"Candidate account successfully created for {user}"
        messages.success(self.request, msg)
        return redirect("login")


class CompanyRegisterView(CreateView):
    model = User
    form_class = CompanyRegisterForm
    template_name = "registration/comp-register.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "company"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        msg = f"Company account successfully created for {user}"
        messages.success(self.request, msg)
        return redirect("login")


class ChooseRegisterView(TemplateView):
    """Asks the user if they are a candidate looking for a job or a company
    giving job offers"""

    template_name = "registration/register.html"
    redirect_authenticated_user = True


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


def logout_user(request):
    logout(request)
    return redirect("login")
