# Generated by Django 5.1.7 on 2025-06-09 08:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_remove_productforcart_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user',)},
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('session_key__isnull', True), ('user__isnull', False)), models.Q(('session_key__isnull', False), ('user__isnull', True)), _connector='OR'), name='user_or_session_key_present'),
        ),
    ]
