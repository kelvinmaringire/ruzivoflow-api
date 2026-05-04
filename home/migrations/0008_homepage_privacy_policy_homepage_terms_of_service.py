# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_alter_homepage_portfolio_items"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="privacy_policy",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="homepage",
            name="terms_of_service",
            field=models.TextField(blank=True, null=True),
        ),
    ]
