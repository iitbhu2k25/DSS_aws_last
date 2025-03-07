# Generated by Django 5.1.6 on 2025-03-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("district_code", models.IntegerField()),
                ("district_name", models.CharField(max_length=30)),
                ("state_short", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state_code", models.IntegerField()),
                ("state_name", models.CharField(max_length=30)),
                ("state_short", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="SubDistrict",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subdistrict_code", models.IntegerField()),
                ("subdistrict_name", models.CharField(max_length=30)),
                ("district_name", models.CharField(max_length=30)),
                ("state_short", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Village",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("village_code", models.IntegerField(unique=True)),
                ("village_name", models.CharField(max_length=100)),
                ("sewage_gap", models.DecimalField(decimal_places=10, max_digits=20)),
                (
                    "mean_temperature",
                    models.DecimalField(decimal_places=10, max_digits=20),
                ),
                (
                    "mean_rainfall",
                    models.DecimalField(decimal_places=10, max_digits=20),
                ),
                ("number_of_tourists", models.IntegerField()),
                (
                    "water_quality_index",
                    models.DecimalField(decimal_places=10, max_digits=20),
                ),
                ("number_of_asi_sites", models.IntegerField()),
                (
                    "gdp_at_current_prices",
                    models.DecimalField(decimal_places=10, max_digits=20),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Weight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sewage_gap", models.FloatField()),
                ("mean_temperature", models.FloatField()),
                ("mean_rainfall", models.FloatField()),
                ("number_of_tourists", models.FloatField()),
                ("water_quality_index", models.FloatField()),
                ("number_of_asi_sites", models.FloatField()),
                ("gdp_at_current_prices", models.FloatField()),
            ],
        ),
    ]
