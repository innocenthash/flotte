# Generated by Django 4.2.13 on 2024-07-24 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWithFlotte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custcode', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type_de_ligne', models.CharField(max_length=50)),
                ('plan_tarifaire', models.CharField(max_length=50)),
                ('localisation', models.CharField(max_length=200)),
                ('card', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='card.card')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Information',
                'verbose_name_plural': 'Informations',
            },
        ),
    ]