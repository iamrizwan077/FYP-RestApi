from django.db import models
from django.core.validators import int_list_validator

# Create your models here.
class NTN(models.Model):
    ntn = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    
class AnomalyInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    description=models.CharField(max_length=500)

# class POS(models.Model):
#     pos = models.IntegerField()
#     ntn = models.ForeignKey(NTN, on_delete=models.PROTECT)
#     user = models.CharField(max_length=256, null=True)
#     password = models.CharField(max_length=256, null=True)

#     class Meta:
#         # This Meta class sets the composite primary key constraint
#         unique_together = ('pos', 'ntn')

class Anomaly(models.Model):
    srb_invoice_id = models.CharField(primary_key=True, max_length=256)
    # pos = models.ForeignKey(POS, to_field="pos", on_delete=models.DO_NOTHING)
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
    tariff_code = models.CharField(null=True, max_length=256, blank=True)
    extra_info = models.CharField(max_length=256, null=True)
    pos_user = models.CharField(max_length=256, null=True)
    pos_pass = models.CharField(max_length=256, null=True)
    is_active =models.BooleanField()
    created_date_time = models.DateTimeField()
    invoice_type = models.IntegerField()
    consider_for_annex = models.IntegerField(null=True)
    anomaly = models.ForeignKey(AnomalyInfo, on_delete=models.PROTECT, null=True)
    # anomaly = models.IntegerField(null=True)

class MissingInvoice(models.Model):
    ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    invoices = models.CharField(validators=[int_list_validator], max_length=256)
    date = models.DateField()

