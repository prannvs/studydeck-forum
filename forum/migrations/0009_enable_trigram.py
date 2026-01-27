from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_make_report_slug_unique'), 
    ]

    operations = [
        TrigramExtension(),
    ]