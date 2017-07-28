# Create your models here.

from django.db import models

from Manager.models import Manager
from Resident.models import Resident

FACILITY_TYPE = (
    ('P', 'استخر'),
    ('A', 'آمفی تئاتر'),
    ('G', 'سالن ورزش'),
    ('B', 'آلاچیق')
)

RESERVE_STATE = {
    ('NC', 'بررسی نشده'),
    ('R', 'رد شده'),
    ('A', 'تایید شده')
}


class Block(models.Model):
    bill_num = models.IntegerField()
    complex = models.ForeignKey(Manager)

    def __str__(self):
        return 'complex: ' + self.complex + ' block: ' + str(self.id)


class Complex(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    manager = models.OneToOneField(Manager)

    def __str__(self):
        return 'name: ' + self.name + ' manager: ' + self.manager


class Facility(models.Model):
    type = models.CharField(max_length=1, choices=FACILITY_TYPE)

    def __str__(self):
        return self.type


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


class Board(models.Model):
    block = models.OneToOneField(Block)

    def __str__(self):
        return self.block + ' board: ' + str(self.id)


class News(models.Model):
    board = models.ForeignKey(Board)
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    Description = models.CharField(max_length=1000)

    def __str__(self):
        return self.board + ' title: ' + self.title


class Event(models.Model):
    board = models.ForeignKey(Board)
    datetime = models.DateTimeField()
    cost = models.IntegerField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.board + ' description: ' + self.description


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
