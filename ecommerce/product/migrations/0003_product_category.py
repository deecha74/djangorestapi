# Generated by Django 4.0.6 on 2024-01-12 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category'),
        ),
    ]
