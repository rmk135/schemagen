# Generated by Django 3.1.4 on 2020-12-25 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schemagen', '0002_field_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemagen.user')),
            ],
        ),
        migrations.CreateModel(
            name='Schema_Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemagen.field')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemagen.schema')),
            ],
        ),
    ]
