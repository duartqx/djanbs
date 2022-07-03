from django.db import models


class PaymentRange(models.IntegerChoices):
    LOW = 1, 'LOW (Up to 1000)' # 'Up to 1000'
    MID_FIRST = 2, 'MID FIRST (1000~2000)' # 'From 1000 to 2000'
    MID_SECOND = 3, 'MID SECOND (2000~3000)' # 'From 2000 to 3000'
    HIGH = 4, 'HIGH (More than 3000)' # 'More than 3000'


class PositionLevel(models.IntegerChoices):
    INTERN = 1, 'INTERN' # Estágio
    JUNIOR = 2, 'JUNIOR' # Junior
    PLENO = 3, 'PLENO' # Pleno
    SENIOR = 4, 'SENIOR' # Senior
    LEAD = 5, 'LEAD' # Tech Lead/Manager


class EducationRequirement(models.IntegerChoices):
    MIDDLE = 1, 'MIDDLE' # Fundamental
    HIGH = 2, 'HIGH' # Ensino Médio
    ASSOCIATE = 3, 'ASSOCIATE' # Tecnólogo
    BACHELOR = 4, 'BACHELOR' # Graduação/Licenciatura
    MASTER = 5, 'MASTER' # MBA/MASTER
    PHD = 6, 'PHD' # Doutorado


def int_to_string(int_choice, integer) -> str:
    for num, string in int_choice.choices: # type: ignore
        if num == integer:
            return string
    return ''
