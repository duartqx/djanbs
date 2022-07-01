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

