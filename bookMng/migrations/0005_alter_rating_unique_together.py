# Generated by Django 4.1.5 on 2023-05-01 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookMng", "0004_alter_rating_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="rating",
            unique_together=set(),
        ),
    ]
