from django.contrib import admin
from .models import Candidact, Company, JobCandidacted, JobOffer

admin.site.register(Candidact)
admin.site.register(Company)
admin.site.register(JobOffer)
admin.site.register(JobCandidacted)

