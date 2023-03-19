# Generated by Django 2.1.5 on 2023-03-19 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20230318_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('commodities', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Commodities')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
