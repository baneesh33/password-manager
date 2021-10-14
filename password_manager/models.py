from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
from django_cryptography.fields import encrypt
from datetime import datetime

User = get_user_model()

class UserPasswords(models.Model):
	uid = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
	password = encrypt(models.CharField(max_length=256))
	category = models.CharField(max_length=256, null=True)
	date = models.DateTimeField(auto_now_add=True)

class SharedPasswordsDetails(models.Model):
	uid = models.ForeignKey(User, on_delete=models.CASCADE)
	shared_with_uid = models.ForeignKey(User, related_name='shared', on_delete=models.CASCADE)
	password = models.ForeignKey(UserPasswords, on_delete=models.CASCADE)
	view_perm = models.BooleanField(default=False)
	edit_perm = models.BooleanField(default=False)
	# date = models.DateTimeField(auto_now_add=True, blank=True)
