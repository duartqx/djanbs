"""djanbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import jobs.views.views # type: ignore
import jobs.views.accounts # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', 
        jobs.views.views.home, 
        name='home'),
    
    path('profile/', 
        jobs.views.views.profile, 
        name='profile'),

    path('profile/edit/', 
        jobs.views.views.profile_edit, 
        name='profile-edit'),

    path('create-offer/<str:pk>/', 
        jobs.views.views.create_job_offer, 
        name='create-offer'),

    path('edit-offer/<str:pk>/', 
        jobs.views.views.edit_job_offer, 
        name='edit-offer'),
    
    path('delete-offer/<str:pk>/', 
        jobs.views.views.delete_job_offer, 
        name='delete-offer'),
    
    path('details-offer/<str:pk>/', 
        jobs.views.views.details_job_offer, 
        name='details-offer'),
    
    path('logout/', 
        jobs.views.accounts.logout_user, 
        name='logout'),
    
    path('login/', 
        jobs.views.accounts.CustomLoginView.as_view(), 
        name='login'),
    
    path('register/', 
        jobs.views.accounts.ChooseRegisterView.as_view(),
        name='register'),
    
    path('register/candidate/', 
        jobs.views.accounts.CandidateRegisterView.as_view(),
        name='register-cand'),
    
    path('register/company/', 
        jobs.views.accounts.CompanyRegisterView.as_view(),
        name='register-comp'),
    
    path('job-candidate/<str:job_id>/', 
        jobs.views.views.candidate_to_job, 
        name='job-candidate'),

    path('delete-job-application/<str:job_id>/',
        jobs.views.views.delete_job_application,
        name='delete-job-application'),

    path('details-cand/<str:jc_id>/',
        jobs.views.views.cand_details,
        name='details-cand'),

]
