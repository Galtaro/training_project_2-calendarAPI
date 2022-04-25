from django.db import migrations


def create_defaults(apps, schema_editor):
    Notification = apps.get_model('events', 'Notification')
    Notification.objects.create(
        description='Do not deliver notification',
        value_time=None

    )


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_defaults)
    ]