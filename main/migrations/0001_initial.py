# Generated by Django 4.2.6 on 2024-10-07 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(default='UTC', max_length=100)),
                ('picture', models.ImageField(blank=True, upload_to='profile_pics/')),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField()),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.contact')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppAccessTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'unique_together': {('id',)},
            },
        ),
    ]
