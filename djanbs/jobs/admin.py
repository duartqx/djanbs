from django.contrib import admin
from .models import Candidact, Company, JobCandidacted, JobOffer, User

admin.site.register(User)
admin.site.register(Candidact)
admin.site.register(Company)
admin.site.register(JobOffer)
admin.site.register(JobCandidacted)

