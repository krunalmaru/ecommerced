# Generated by Django 4.1.4 on 2022-12-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_product_packing_cost_product_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField()),
            ],
        ),
    ]
