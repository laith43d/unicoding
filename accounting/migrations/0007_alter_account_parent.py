# Generated by Django 4.0.6 on 2022-08-01 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_alter_account_code_alter_account_full_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='accounting.account'),
        ),
    ]
