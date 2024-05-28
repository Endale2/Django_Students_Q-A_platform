# Generated by Django 5.0.4 on 2024-04-25 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alpha', '0009_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='alpha.questions'),
        ),
        migrations.AlterField(
            model_name='replies',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='alpha.answers'),
        ),
    ]
