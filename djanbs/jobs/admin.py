from django.contrib import admin
from .models import Candidate, Company, JobApplied, JobOffer, User

admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(JobOffer)
admin.site.register(JobApplied)
