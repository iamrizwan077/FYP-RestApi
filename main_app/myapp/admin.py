from django.contrib import admin
from myapp import models

# Register your models here.
admin.site.register(models.Anomaly)
admin.site.register(models.NTN)
admin.site.register(models.MissingInvoice)