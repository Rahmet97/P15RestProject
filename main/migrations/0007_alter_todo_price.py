# Generated by Django 4.2.7 on 2023-11-15 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_todo_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]