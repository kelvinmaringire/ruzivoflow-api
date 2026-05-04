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
            field=wagtail.fields.RichTextField(blank=True, features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'strikethrough', 'superscript', 'subscript', 'ol', 'ul', 'hr', 'blockquote', 'code', 'link', 'document-link', 'image', 'embed'], null=True),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="terms_of_service",
            field=wagtail.fields.RichTextField(blank=True, features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'strikethrough', 'superscript', 'subscript', 'ol', 'ul', 'hr', 'blockquote', 'code', 'link', 'document-link', 'image', 'embed'], null=True),
        ),
    ]
