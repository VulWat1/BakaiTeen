from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ACCOUNT_CHOICES = (
        ('child', 'Child'),
        ('parent', 'Parent'),
    )
    coin = models.IntegerField('Монеты', default='0')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)
    def __str__(self):
        return f"{self.user.username} - {self.account_type}" 