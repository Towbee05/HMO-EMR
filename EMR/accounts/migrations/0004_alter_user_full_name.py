# Generated by Django 5.2.1 on 2025-06-06 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_plans_user_full_name_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(max_length=140, verbose_name='Full Name'),
        ),
    ]
