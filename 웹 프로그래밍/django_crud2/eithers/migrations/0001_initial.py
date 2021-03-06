# Generated by Django 2.2.7 on 2019-11-05 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('issue_a', models.CharField(max_length=200)),
                ('issue_b', models.CharField(max_length=200)),
                ('image_a', models.ImageField(blank=True, upload_to='eithers/images')),
                ('image_b', models.ImageField(blank=True, upload_to='eithers/images')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pick', models.IntegerField()),
                ('comment', models.TextField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eithers.Question')),
            ],
        ),
    ]
