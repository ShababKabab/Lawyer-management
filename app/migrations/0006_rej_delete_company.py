# Generated by Django 4.0.2 on 2023-04-16 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_company_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='rej',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('number', models.IntegerField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
