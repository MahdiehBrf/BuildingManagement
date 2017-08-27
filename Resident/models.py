# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from MySite.models import Facility, Unit
from MyUser.models import Member

RESERVE_STATE = {
    ('NC', 'بررسی نشده'),
    ('R', 'رد شده'),
    ('A', 'تایید شده')
}

class Resident(models.Model):
    member = models.OneToOneField(Member)
    member_count = models.IntegerField()
    car_count = models.IntegerField()
    unit = models.OneToOneField(Unit)
    #email = models.EmailField()

    def __str__(self):
        return str(self.member)

#     # don't forget to write save
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Resident.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.resident.save()


class Reserve(models.Model):
    reserve_date = models.DateTimeField(primary_key=True)
    # duration = models.IntegerField()  # hours
    use_finishDate = models.DateTimeField()
    use_startDate = models.DateTimeField()
    cost = models.IntegerField()
    state = models.CharField(max_length=2, choices=RESERVE_STATE)
    resident = models.ForeignKey(Resident)
    facility = models.ForeignKey(Facility)

    def __str__(self):
        return 'resident: ' + str(self.resident) + ' facility: ' + str(self.facility) + ' reserve date:' + str(self.reserve_date)


class Receipt(models.Model):
    date = models.DateField()
    cost = models.IntegerField(null=True)
    event_cost = models.IntegerField(null=True)
    facility_cost = models.IntegerField(null=True)
    common_bills_cost = models.IntegerField()
    resident= models.ForeignKey(Resident)

    def __str__(self):
        return 'date: ' + str(self.date) + ' cost: ' + str(self.cost)


class Account(models.Model):
    cash = models.PositiveIntegerField()
    resident = models.OneToOneField(Resident)

    def __str__(self):
        return 'resident: ' + str(self.resident)


class PayByBank(models.Model):
    date = models.DateField(primary_key=True)
    amount = models.IntegerField()
    resident = models.OneToOneField(Resident)
    receipt = models.OneToOneField(Receipt)

    def __str__(self):
        return 'resident: ' + str(self.resident) + ' date: ' + str(self.date)


class PayByAccount(models.Model):
    date = models.DateField(primary_key=True)
    amount = models.IntegerField()
    account = models.OneToOneField(Account)
    receipt = models.OneToOneField(Receipt)

    def __str__(self):
        return str(self.account) + ' date: ' + str(self.date)
