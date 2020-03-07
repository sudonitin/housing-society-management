from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group)

admin.site.site_header = "Manage My Society"
admin.site.site_title = "Administration Page for MMS"