from django.db import models

# Create your models here.
class NTN(models.Model):
    ntn = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)

class Anomaly(models.Model):
    srb_invoice_id = models.BigIntegerField(primary_key=True)
    pos_id = models.IntegerField()
    ntn_id = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    invoice_date = models.DateTimeField()
    invoice_no = models.BigIntegerField()    
    rate_value = models.FloatField()
    sales_value = models.FloatField()
    sales_tax = models.FloatField()
    consumer_name = models.CharField(max_length=256, null=True)
    # consumer_ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    consumer_ntn = models.IntegerField(null=True)
    consumer_address = models.CharField(max_length=256, null=True)
    tariff_code = models.IntegerField(null=True)
    extra_info = models.CharField(max_length=256, null=True)
    pos_user = models.CharField(max_length=256)
    pos_pass = models.CharField(max_length=256, null=True)
    is_active =models.BooleanField()
    created_date_time = models.DateTimeField()
    invoice_type = models.IntegerField()
    consider_for_annex = models.IntegerField()
    anomaly = models.BooleanField(default=False)

class MissingInvoice(models.Model):
    ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    invoice = models.IntegerField()
    date = models.DateTimeField()