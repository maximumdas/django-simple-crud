# Generated by Django 3.0.8 on 2020-07-26 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20200726_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('profil_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='ToDoList',
        ),
    ]