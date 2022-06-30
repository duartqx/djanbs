from django.contrib.auth.models import User
from django.db import models


class PaymentRange(models.IntegerChoices):
    LOW = 1 # Up to 1000
    MID_FIRST = 2 # From 1000 to 2000
    MID_SECOND = 3 # From 2000 to 3000
    HIGH = 4 # More than 3000


class PositionLevel(models.IntegerChoices):
    INTERN = 1 # Estágio
    JUNIOR = 2 # Junior
    PLENO = 3 # Pleno
    SENIOR = 4 # Senior
    LEAD = 5 # Tech Lead/Manager


class EducationRequirement(models.IntegerChoices):
    MIDDLE = 1 # Fundamental
    HIGH = 2 # Ensino Médio
    ASSOCIATE = 3 # Tecnólogo
    BACHELOR = 4 # Graduação/Licenciatura
    MASTER = 5 # MBA/MASTER
    PHD = 6 # Doutorado


class Company(models.Model):
    ''' A Company that may post JobOffer to Candidacts '''
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    site = models.URLField()

    def __str__(self):
        return self.name


class Candidact(models.Model):
    ''' A user looking for JobOffers '''
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=120)
    payment_range = models.IntegerField(choices=PaymentRange.choices)
    education = models.IntegerField(choices=EducationRequirement.choices)
    position_level = models.IntegerField(choices=PositionLevel.choices)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class JobOffer(models.Model):
    ''' A Company creates and has many JobOffers '''
    name = models.CharField(max_length=125)
    location = models.CharField(max_length=50)
    description = models.TextField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    payment_range = models.IntegerField(choices=PaymentRange.choices)
    education_req = models.IntegerField(choices=EducationRequirement.choices)
    position_level = models.IntegerField(choices=PositionLevel.choices)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class JobCandidacted(models.Model):
    ''' When a candidact candidacts himself to a JobOffer we write this
    relationship into the database for future access by the site
    administration, companies or the candidact himself '''
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    candidact = models.ForeignKey(Candidact, on_delete=models.SET_NULL, null=True)
    date_candidacted = models.DateTimeField(auto_now_add=True, null=True)

    def _get_cndct_count(self):
        ''' Finds out how many applied to each job_offer '''
        return JobCandidacted.objects.filter( # type: ignore
                job_offer=self.job_offer).values(
                    "candidact").distinct().count() 

    def __str__(self):
        return f'{self.job_offer} ({self._get_cndct_count()} applied) - {self.candidact}' # type: ignore
