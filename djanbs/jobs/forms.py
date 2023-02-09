from .choices import EducationRequirement, PaymentRange, PositionLevel
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db import transaction


from .models import Candidate, Company, JobApplied, JobOffer, User


class CandidateRegisterForm(UserCreationForm):

    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=120)
    payment_range = forms.CharField(
        max_length=50, widget=forms.Select(choices=PaymentRange.choices)
    )
    education = forms.CharField(
        max_length=50, widget=forms.Select(choices=EducationRequirement.choices)
    )
    position_level = forms.CharField(
        max_length=50, widget=forms.Select(choices=PositionLevel.choices)
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "payment_range",
            "education",
            "position_level",
        ]

    @transaction.atomic
    def save(self, create=True):
        user = super().save(commit=False)
        user.is_candidate = True
        user.save()

        if create:
            candidate = Candidate.objects.create(  # type: ignore
                user=user,
                first_name=self.cleaned_data.get("first_name"),
                last_name=self.cleaned_data.get("last_name"),
                payment_range=self.cleaned_data.get("payment_range"),
                education=self.cleaned_data.get("education"),
                position_level=self.cleaned_data.get("position_level"),
            )
        else:
            candidate = Candidate.objects.filter(user=user).update(  # type: ignore
                user=user,
                first_name=self.cleaned_data.get("first_name"),
                last_name=self.cleaned_data.get("last_name"),
                payment_range=self.cleaned_data.get("payment_range"),
                education=self.cleaned_data.get("education"),
                position_level=self.cleaned_data.get("position_level"),
            )

        if Group.objects.filter(name="candidate").exists():
            group = Group.objects.get(name="candidate")
            user.groups.add(group)
        return user


class CompanyRegisterForm(UserCreationForm):

    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    site = forms.URLField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "email",
            "password1",
            "password2",
            "name",
            "site",
        ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        company = Company.objects.create(  # type: ignore
            user=user,
            email=self.cleaned_data.get("email"),
            name=self.cleaned_data.get("name"),
            site=self.cleaned_data.get("site"),
        )
        if Group.objects.filter(name="company").exists():
            group = Group.objects.get(name="company")
            user.groups.add(group)
        return user


class JobOfferCreationForm(forms.ModelForm):
    """A form that companies see when creating new job offers"""

    class Meta:
        model = JobOffer
        exclude = ("company",)


class JobCandidateForm(forms.ModelForm):
    """A form that the user submits when candidating to a job offer"""

    class Meta:
        model = JobApplied
        exclude = ("candidate", "job_offer")
