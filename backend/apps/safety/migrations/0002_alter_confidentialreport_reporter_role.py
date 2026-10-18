from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('safety', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confidentialreport',
            name='reporter_role',
            field=models.CharField(
                choices=[
                    ('student', 'Учень / учениця'),
                    ('parent', 'Батьки / законні представники'),
                    ('teacher', 'Педагогічний працівник'),
                    ('witness', 'Свідок події'),
                    ('anonymous', 'Анонімно'),
                ],
                default='anonymous',
                max_length=20,
                verbose_name='Статус заявника',
            ),
        ),
    ]
