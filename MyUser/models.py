from django.contrib.auth.models import User
from django.db import models


MESSAGE_THEME_TYPE = (
    (0, 'بدون قالب'),
    (1, 'قالب 1'),
    (2, 'قالب 2'),
)


class Member(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=12)
    image = models.FileField(upload_to='static/images/profile_picture',
                              default='../static/images/user_profile_female.jpg')

    def __str__(self):
        return self.user.username

    # don't forget to write save


class Message(models.Model):
    text = models.CharField(max_length=1000)
    theme_type = models.IntegerField(choices=MESSAGE_THEME_TYPE)
    sender = models.ForeignKey(Member, related_name='sender')
    receiver = models.ForeignKey(Member, related_name='receiver')

    def __str__(self):
        return 'sender: ' + str(self.sender) + ' receiver: ' + str(self.receiver)
