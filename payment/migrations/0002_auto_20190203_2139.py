# Generated by Django 2.1.1 on 2019-02-03 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated')),
                ('name', models.CharField(default='demo', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated')),
                ('product', models.CharField(max_length=255)),
                ('name', models.CharField(default='demo', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.SubscriptionPlan'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentToken'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
