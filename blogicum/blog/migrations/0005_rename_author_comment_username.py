# Generated by Django 3.2.16 on 2024-01-31 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='username',
        ),
    ]
