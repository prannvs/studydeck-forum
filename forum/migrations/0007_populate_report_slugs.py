from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    Report = apps.get_model('forum', 'Report')

    for report in Report.objects.all():
        report.slug = str(uuid.uuid4())
        report.save()

class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_add_report_slug_nullable'), 
    ]

    operations = [
        migrations.RunPython(gen_uuid),
    ]