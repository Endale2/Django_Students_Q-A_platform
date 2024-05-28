# Generated by Django 5.0.2 on 2024-04-17 07:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpha', '0005_rename_department_name_course_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='alpha.questions'),
        ),
        migrations.AlterField(
            model_name='answers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='replies',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='alpha.answers'),
        ),
        migrations.AlterField(
            model_name='replies',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL),
        ),
    ]