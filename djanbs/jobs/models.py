from .choices import EducationRequirement, PaymentRange, PositionLevel
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import EducationRequirement, PaymentRange, PositionLevel#, int_to_string


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    is_company = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Candidate(models.Model):
    ''' A user looking for JobOffers '''
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=120, null=True)
    payment_range = models.IntegerField(choices=PaymentRange.choices, null=True)
    education = models.IntegerField(choices=EducationRequirement.choices, null=True)
    position_level = models.IntegerField(choices=PositionLevel.choices, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Company(models.Model):
    ''' A Company that may post JobOffer to Candidates '''
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    site = models.URLField(null=True)

    def __str__(self):
        return self.name


class JobOffer(models.Model):
    ''' A Company creates and has many JobOffers '''
    name = models.CharField(max_length=125)
    location = models.CharField(max_length=50)
    description = models.TextField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    payment_range = models.IntegerField(choices=PaymentRange.choices)
    education_req = models.IntegerField(choices=EducationRequirement.choices)
    position_level = models.IntegerField(choices=PositionLevel.choices)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class JobApplied(models.Model):
    ''' When a candidate candidates himself to a JobOffer we write this
    relationship into the database for future access by the site
    administration, companies or the candidate himself '''
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    date_candidated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job_offer', 'candidate'], name='only apply once')
        ]

    def education(self):
        return self.job_offer.education_req <= self.candidate.education # type: ignore

    def position_level(self):
        return self.job_offer.position_level <= self.candidate.position_level # type: ignore
    
    def payment_range(self):
        return self.job_offer.payment_range >= self.candidate.payment_range # type: ignore
    
    def cand_pontuation(self):
        cand_points = []
        fields = [
            (self.job_offer.education_req, self.candidate.education), # type: ignore
            (self.job_offer.position_level, self.candidate.position_level), # type: ignore
            (self.candidate.payment_range, self.job_offer.payment_range), # type: ignore
            ]
        for i, j in fields:
            if i < j: cand_points.append(2)
            elif i == j: cand_points.append(1)
            else: cand_points.append(0)
        return sum(cand_points)

    def _get_cndct_count(self):
        ''' Finds out how many applied to each job_offer '''
        return JobCandidated.objects.filter( # type: ignore
                job_offer=self.job_offer).values(
                    "candidate").distinct().count() 

    def __str__(self):
        return f'{self.job_offer} ({self._get_cndct_count()} applied) - {self.candidate}' # type: ignore
        #return f'{self.job_offer}'
