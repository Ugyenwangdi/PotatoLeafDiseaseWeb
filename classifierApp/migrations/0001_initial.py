# Generated by Django 4.0.4 on 2022-05-16 15:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagepath', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('predicted', models.TextField()),
                ('confidence', models.IntegerField(blank=True, default=0, null=True)),
                ('saved', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-saved',),
            },
        ),
    ]
