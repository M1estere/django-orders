# Generated by Django 5.1.4 on 2025-02-07 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('ready', 'Готово'), ('paid', 'Оплачено')], default='pending', max_length=10)),
                ('items', models.ManyToManyField(to='orders.item')),
            ],
        ),
    ]
