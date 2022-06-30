# Generated by Django 4.0.5 on 2022-06-29 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0011_rename_candidacts_jobcandidacted_candidact'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidact',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobcandidacted',
            name='date_candidacted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]