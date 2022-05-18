# Generated by Django 4.0.4 on 2022-05-17 12:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classifierApp', '0003_rename_imagename_result_imagepath'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagename', models.TextField()),
                ('imagepath', models.ImageField(blank=True, null=True, upload_to='')),
                ('predicted', models.TextField()),
                ('confidence', models.IntegerField(blank=True, default=0, null=True)),
                ('saved', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]