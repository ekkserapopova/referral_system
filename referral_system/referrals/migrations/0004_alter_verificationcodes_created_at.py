# Generated by Django 5.1.3 on 2024-12-01 18:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0003_alter_verificationcodes_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcodes',
            name='created_at',
            field=models.DateTimeField(auto_created=datetime.datetime(2024, 12, 1, 21, 48, 1, 256932)),
        ),
    ]