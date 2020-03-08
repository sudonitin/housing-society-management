from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SocietyDetail(models.Model):
    address = models.CharField(max_length = 1000, null = False)
    secretary = models.ForeignKey(User, on_delete=models.CASCADE)
    society_name = models.CharField(max_length = 100, null = False)

    def __str__(self):
        return self.society_name 

class Forum(models.Model):
    title = models.CharField(max_length = 100, null = False)
    description = models.CharField(max_length = 1000, null = False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.IntegerField( null=False)
    society = models.ForeignKey(SocietyDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' | ' + str(self.creator) + ' | ' + str(self.society)


class Owner(models.Model):
    society = models.ForeignKey(SocietyDetail, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    flat_no = models.CharField(max_length = 20, null = False)

    def __str__(self):
        return str(self.society) + ' | ' + str(self.name) + ' | ' + self.flat_no

class MaintenanceBill(models.Model):
    for_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    society = models.ForeignKey(SocietyDetail, on_delete=models.CASCADE)
    description = models.CharField(max_length = 100, null = False)
    paid = models.CharField(max_length = 3, default = 'no')

    def __str__(self):
        return str(self.society) + ' | ' + str(self.for_owner)