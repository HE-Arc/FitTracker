from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fittrackerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='rank_in_program',
            field=models.IntegerField(default=1),
        ),
    ]
