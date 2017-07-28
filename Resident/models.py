# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from MyUser.models import Member


class Unit(models.Model):
    area = models.IntegerField()


class Resident(models.Model):
    member = models.OneToOneField(Member)
    member_count = models.IntegerField()
    car_count = models.IntegerField()
    unit = models.OneToOneField(Unit)

    def __str__(self):
        return self.member

    # don't forget to write save


