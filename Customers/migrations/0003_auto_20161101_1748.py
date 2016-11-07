# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-01 22:48
from __future__ import unicode_literals

import Customers.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Customers', '0002_auto_20160713_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_date', models.DateField(blank=True, null=True)),
                ('time_slot', models.CharField(choices=[(b'2:00-4:00', b'2-4'), (b'11:00-1:00', b'11-1'), (b'12:00-2:00', b'12-2'), (b'8:00-10:00', b'8-10'), (b'10:00-12:00', b'10-12'), (b'9:00-11:00', b'9-11'), (b'1:00-3:00', b'1-3')], default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('modified_by', models.CharField(default=1, max_length=50)),
                ('jobId', models.AutoField(primary_key=True, serialize=False)),
                ('jobStreet', models.CharField(max_length=25)),
                ('jobCity', models.CharField(max_length=20)),
                ('jobState', models.CharField(max_length=2)),
                ('jobZip', models.CharField(max_length=5)),
                ('stories', models.IntegerField()),
                ('access', models.CharField(max_length=20)),
                ('problem', models.CharField(max_length=200)),
                ('notes', models.CharField(blank=True, max_length=150)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('assigned_to', models.CharField(blank=True, choices=[(b'Evan', b'Evan'), (b'Chalie', b'Chalie'), (b'John', b'John'), (b'Barry', b'Barry'), (b'Service', b'Service')], default='', max_length=20)),
                ('contract', models.FileField(blank=True, upload_to=Customers.models.upload_location)),
                ('crew_assigned', models.CharField(blank=True, choices=[(b'Evan', b'Evan'), (b'Chalie', b'Chalie'), (b'John', b'John'), (b'Barry', b'Barry'), (b'Service', b'Service'), (b'Jake', b'Jake'), (b'Corey', b'Corey'), (b'Chris', b'Chris'), (b'Sub', b'Sub')], default='', max_length=50)),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('latlng', models.CharField(blank=True, default='', max_length=100)),
                ('lat', models.FloatField(blank=True, default=0, max_length=100)),
                ('lng', models.FloatField(blank=True, default=0, max_length=100)),
            ],
            options={
                'ordering': ['-created', '-modified'],
            },
        ),
        migrations.RemoveField(
            model_name='jobsite',
            name='customer',
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AddField(
            model_name='customer',
            name='fullName',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='lat',
            field=models.FloatField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='latlng',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='lng',
            field=models.FloatField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='modified_by',
            field=models.CharField(default=1, max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='source',
            field=models.CharField(choices=[(b'NA', b'Not Applicable'), (b'AL', b"Angie's List"), (b'CO', b'Contractor'), (b'GO', b'Google'), (b'OC', b'Old Customer'), (b'OT', b'Other'), (b'RC', b'Recco'), (b'RE', b'Realtor'), (b'WS', b'Website'), (b'YL', b'Yelp')], default=b'NA', max_length=20),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone2',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.DeleteModel(
            name='Jobsite',
        ),
        migrations.AddField(
            model_name='workorder',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customers.Customer'),
        ),
        migrations.AddField(
            model_name='workorder',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='workorder_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customers.WorkOrder'),
        ),
    ]