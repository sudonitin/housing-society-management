from django.db import models
from django.contrib.auth.models import User
# Create your models here.

User._meta.get_field('email')._unique = True
User._meta.get_field('email')._null = False
User._meta.get_field('first_name')._null = True
User._meta.get_field('last_name')._null = True