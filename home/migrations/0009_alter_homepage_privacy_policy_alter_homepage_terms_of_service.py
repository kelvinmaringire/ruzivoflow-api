from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_homepage_privacy_policy_homepage_terms_of_service"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="privacy_policy",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="terms_of_service",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
