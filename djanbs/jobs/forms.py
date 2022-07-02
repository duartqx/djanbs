from .choices import EducationRequirement, PaymentRange, PositionLevel
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


from .models import Candidact, Company, JobOffer, User


class CandidactRegisterForm(UserCreationForm):
    
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=120)
    payment_range = forms.CharField(max_length=50, 
            widget=forms.Select(choices=PaymentRange.choices))
    education = forms.CharField(max_length=50, 
            widget=forms.Select(choices=EducationRequirement.choices))
    position_level = forms.CharField(max_length=50, 
            widget=forms.Select(choices=PositionLevel.choices))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_candidact = True
        user.save()
        candidact = Candidact.objects.create( # type: ignore
                user=user,
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                payment_range=self.cleaned_data.get('payment_range'),
                education=self.cleaned_data.get('education'),
                position_level=self.cleaned_data.get('position_level'),
                ) 
        print(candidact)
        return user


class CompanyRegisterForm(UserCreationForm):

    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    site = forms.URLField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
        company = Company.objects.create( # type: ignore
                user=user,
                email=self.cleaned_data.get('email'),
                name=self.cleaned_data.get('name'),
                site=self.cleaned_data.get('site'),
            )
        print(company)
        return user

class JobOfferCreationForm(forms.ModelForm):
    ''' A form that companies see when creating new job offers '''
    class Meta():
        model = JobOffer
        exclude = ('company',)
