from django.contrib import admin
from .models import SocietyDetail, Forum, Owner, MaintenanceBill
# Register your models here.


admin.site.register(SocietyDetail)
admin.site.register(Forum)
admin.site.register(Owner)
admin.site.register(MaintenanceBill)