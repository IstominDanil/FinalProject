# Generated by Django 4.1.7 on 2023-03-12 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='posts', through='final.PostCategory', to='final.category'),
        ),
    ]
