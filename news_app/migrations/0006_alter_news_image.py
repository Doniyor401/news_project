# Generated by Django 5.0.1 on 2024-01-18 18:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news_app", "0005_alter_news_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="image",
            field=models.ImageField(upload_to="news/images"),
        ),
    ]