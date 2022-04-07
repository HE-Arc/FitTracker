from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fittrackerapp', '0002_alter_exercise_rank_in_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]