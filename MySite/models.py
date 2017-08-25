# Create your models here.

from django.db import models

from Manager.models import Manager

FACILITY_TYPE = (
    ('P', 'استخر'),
    ('A', 'آمفی تئاتر'),
    ('G', 'سالن ورزش'),
    ('B', 'آلاچیق')
)



class Unit(models.Model):
    area = models.IntegerField()
    block = models.ForeignKey('Block')

    def __str__(self):
        return self.block + ' unit:' + str(self.id)

class Block(models.Model):
    complex = models.ForeignKey('Complex')
    unit_number = models.IntegerField()

    def __str__(self):
        return 'complex: ' + str(self.complex) + ' block: ' + str(self.id)


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
