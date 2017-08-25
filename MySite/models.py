# Create your models here.

from django.db import models

from Manager.models import Manager

FACILITY_TYPE = (
    ('P', 'استخر'),
    ('A', 'آمفی تئاتر'),
    ('G', 'سالن ورزش'),
    ('B', 'آلاچیق')
)

BILL_TYPE = (
    ('W', 'آب'),
    ('E', 'برق'),
    ('G', 'گاز'),
    ('P', 'تلفن')
)



class Unit(models.Model):
    area = models.IntegerField()
    block = models.ForeignKey('Block')

class Block(models.Model):
    complex = models.ForeignKey('Complex')

    def __str__(self):
        return 'complex: ' + str(self.complex) + ' block: ' + str(self.id)

class Bill(models.Model):
    type = models.CharField(max_length=1, choices=BILL_TYPE)
    num = models.IntegerField()
    cost = models.IntegerField()
    date = models.DateField()
    block = models.ForeignKey(Block)

    def str(self):
        return 'block' + str(self.block) + ' num: ' + str(self.num)


class Complex(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    manager = models.OneToOneField(Manager)

    def __str__(self):
        return 'name: ' + self.name + ' manager: ' + str(self.manager)


class Facility(models.Model):
    type = models.CharField(max_length=20)
    block = models.ForeignKey('Block')
    cost = models.IntegerField()


    def __str__(self):
        return self.type


class Board(models.Model):
    block = models.OneToOneField(Block)

    def __str__(self):
        return str(self.block) + ' board: ' + str(self.id)


class News(models.Model):
    board = models.ForeignKey(Board)
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.board) + ' title: ' + str(self.title)


class Event(models.Model):
    board = models.ForeignKey(Board)
    date = models.DateField()
    cost = models.IntegerField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.board) + ' description: ' + self.description
