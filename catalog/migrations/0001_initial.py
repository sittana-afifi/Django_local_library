# Generated by Django 3.2.7 on 2021-10-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModelName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_field_name', models.CharField(help_text='Enter field documentation', max_length=20)),
            ],
            options={
                'ordering': ['-my_field_name'],
            },
        ),
    ]