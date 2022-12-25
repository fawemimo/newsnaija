# Generated by Django 4.1.4 on 2022-12-20 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsCategory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Category name"),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="format: required, letters, numbers, underscore, or hyphens",
                        max_length=255,
                        verbose_name="category safe URL",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "date_updated",
                    models.DateTimeField(
                        auto_now=True, help_text="format: Y-m-d H:M:S"
                    ),
                ),
            ],
            options={
                "verbose_name": "News Category",
                "verbose_name_plural": "News Categories",
                "ordering": ("-date_created",),
            },
        ),
        migrations.CreateModel(
            name="PostNews",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("content", tinymce.models.HTMLField()),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        help_text="format: it could be links or person name",
                        max_length=255,
                        null=True,
                        verbose_name="News source",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("published", "Published")],
                        default="published",
                        max_length=50,
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "slug",
                    models.SlugField(
                        max_length=255,
                        unique_for_date="date_created",
                        verbose_name="url link related to title",
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(
                        auto_now=True, help_text="format: Y-m-d H:M:S"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="news.newscategory",
                        verbose_name="News Category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Post News",
                "verbose_name_plural": "Post News",
                "ordering": ("-date_created",),
            },
        ),
        migrations.CreateModel(
            name="PostNewsMedia",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "images",
                    models.ImageField(
                        blank=True,
                        help_text="format: optional,not neccessary to upload pics",
                        null=True,
                        upload_to="posts/news",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        help_text="format: optional,not neccessary to upload",
                        null=True,
                        upload_to="posts/files",
                        verbose_name="videos/audio/docs/pdf",
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(
                        help_text="format: required, max-255",
                        max_length=255,
                        verbose_name="alternative text",
                    ),
                ),
                (
                    "is_feature",
                    models.BooleanField(
                        default=False,
                        help_text="format: default=false, true=default image",
                        verbose_name="Post News display image/files",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="format: Y-m-d H:M:S",
                        verbose_name="post news visibility",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="format: Y-m-d H:M:S",
                        verbose_name="date post news created",
                    ),
                ),
                (
                    "postnews",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="news.postnews",
                    ),
                ),
            ],
            options={
                "verbose_name": "Post News Media",
                "verbose_name_plural": "Post News Media",
            },
        ),
    ]