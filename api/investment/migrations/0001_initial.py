# Generated by Django 3.0.5 on 2020-04-26 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invested_amount', models.FloatField()),
                ('user_share', models.FloatField()),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='company.Company')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
