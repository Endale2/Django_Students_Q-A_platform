# Generated by Django 5.0.4 on 2024-04-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpha', '0012_remove_news_comment_newscomment_news_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]
