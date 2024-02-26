from django.db import models
from django.core.validators import int_list_validator

# Create your models here.
class NTN(models.Model):
    ntn = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    

class Anomaly(models.Model):
    srb_invoice_id = models.CharField(primary_key=True, max_length=256)
    pos_id = models.IntegerField()
    ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    invoice_date = models.DateTimeField()
    invoice_no = models.CharField(max_length=256)    
    rate_value = models.FloatField()
    sales_value = models.FloatField()
    sales_tax = models.FloatField()
    consumer_name = models.CharField(max_length=256, null=True)
    # consumer_ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    consumer_ntn = models.IntegerField(null=True)
    consumer_address = models.CharField(max_length=256, null=True)
    tariff_code = models.IntegerField(null=True)
    extra_info = models.CharField(max_length=256, null=True)
    pos_user = models.CharField(max_length=256, null=True)
    pos_pass = models.CharField(max_length=256, null=True)
    is_active =models.BooleanField()
    created_date_time = models.DateTimeField()
    invoice_type = models.IntegerField()
    consider_for_annex = models.IntegerField(null=True)
    anomaly = models.BooleanField(default=False)


class MissingInvoice(models.Model):
    ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    invoices = models.CharField(validators=[int_list_validator], max_length=256)
    date = models.DateField()