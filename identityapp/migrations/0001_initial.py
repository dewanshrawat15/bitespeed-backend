# Generated by Django 4.2.2 on 2023-06-18 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('phoneNumber', models.PositiveBigIntegerField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('linkedId', models.IntegerField(null=True)),
                ('linkPrecedence', models.CharField(choices=[(1, 'primary'), (2, 'secondary')], default=1, max_length=16)),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('deletedAt', models.DateTimeField(null=True)),
            ],
        ),
    ]
