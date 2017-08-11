# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from MyUser.models import Member


class Manager(models.Model):
    member = models.OneToOneField(Member)
    bank_account_num = models.IntegerField()

    def __str__(self):
        return str(self.member)

    # don't forget to write save
