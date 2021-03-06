from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rank_in_program', models.IntegerField()),
                ('number_of_set', models.IntegerField()),
                ('label_data', models.CharField(max_length=50)),
                ('indication', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fittrackerapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fittrackerapp.discipline')),
                ('owner', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('validated', models.BooleanField(default=False)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fittrackerapp.program')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise_Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fittrackerapp.exercise')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fittrackerapp.program')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='program',
            field=models.ManyToManyField(through='fittrackerapp.Exercise_Program', to='fittrackerapp.Program'),

        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_in_set', models.IntegerField()),
                ('value', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fittrackerapp.exercise')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fittrackerapp.training')),
            ],
        ),
    ]
