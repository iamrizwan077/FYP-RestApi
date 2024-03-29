# Generated by Django 5.0.2 on 2024-03-06 05:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_alter_anomaly_tariff_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="anomaly",
            options={"verbose_name": "Anomaly", "verbose_name_plural": "Anomalies"},
        ),
        migrations.AlterModelOptions(
            name="anomalyinfo",
            options={
                "verbose_name": "Anomaly Info",
                "verbose_name_plural": "Anomaly Infos",
            },
        ),
        migrations.AlterModelOptions(
            name="missinginvoice",
            options={
                "verbose_name": "Missing Invoice",
                "verbose_name_plural": "Missing Invoices",
            },
        ),
        migrations.AlterModelOptions(
            name="ntn",
            options={"verbose_name": "NTN", "verbose_name_plural": "NTNs"},
        ),
        migrations.AlterField(
            model_name="anomaly",
            name="consumer_ntn",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="anomaly",
            name="invoice_type",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="anomaly",
            name="rate_value",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="anomaly",
            name="tariff_code",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
