# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from MyUser.models import Member
SUBJECT_CHOICES = (
    ('E', 'خطا در سامانه'),
    ('S', 'پیشنهاد امکانات جدید یا تغییر'),
    ('Q', 'سوال و راهنمایی'),
    ('C', 'شکایات'),
    ('O','سایر')
)

STATE_CHOICES = (
    ('W', 'در صف انتظار'),
    ('C', 'بررسی شده')
)


class Manager(models.Model):
    member = models.OneToOneField(Member)
    bank_account_num = models.IntegerField()

    def __str__(self):
        return str(self.member)

    # don't forget to write save


class Request(models.Model):
    manager = models.ForeignKey(Manager)
    title = models.CharField(max_length=20)
    subject = models.CharField(max_length= 1, choices=SUBJECT_CHOICES)
    text = models.TextField()
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
