# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from MySite.models import Facility
from MyUser.models import Member

RESERVE_STATE = {
    ('NC', 'بررسی نشده'),
    ('R', 'رد شده'),
    ('A', 'تایید شده')
}


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


class Reserve(models.Model):
    reserve_date = models.DateTimeField(primary_key=True)
    duration = models.IntegerField()  # hours
    use_date = models.DateTimeField()
    cost = models.IntegerField()
    state = models.CharField(max_length=1, choices=RESERVE_STATE)
    resident = models.OneToOneField(Resident)
    facility = models.OneToOneField(Facility)

    def __str__(self):
        return 'resident: ' + self.resident + ' facility: ' + self.facility + ' reserve date:' + str(self.reserve_date)


class Receipt(models.Model):
    date = models.DateField()
    cost = models.IntegerField(null=True)
    event_cost = models.IntegerField(null=True)
    facility_cost = models.IntegerField(null=True)
    common_bills_cost = models.IntegerField()

    def __str__(self):
        return 'date: ' + str(self.date) + ' cost: ' + str(self.cost)


class Account(models.Model):
    cash = models.IntegerField()
    resident = models.OneToOneField(Resident)

    def __str__(self):
        return 'resident: ' + self.resident


class PayByBank(models.Model):
    date = models.DateField(primary_key=True)
    amount = models.IntegerField()
    resident = models.OneToOneField(Resident)
    receipt = models.OneToOneField(Receipt)

    def __str__(self):
        return 'resident: ' + self.resident + ' date: ' + str(self.date)


class PayByAccount(models.Model):
    date = models.DateField(primary_key=True)
    amount = models.IntegerField()
    account = models.OneToOneField(Account)
    receipt = models.OneToOneField(Receipt)

    def __str__(self):
        return self.account + ' date: ' + str(self.date)
