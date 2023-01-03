from django.db import models
from accounts.models import User
from django.urls import reverse
from uuid import uuid4
from tinymce.models import HTMLField

class NewsCategory(models.Model):
    """Model definition for NewsCategory."""

    id=models.UUIDField(primary_key=True,default=uuid4)
    name = models.CharField(verbose_name="Category name", max_length=255)
    slug = models.SlugField(
        max_length=255,
        verbose_name=("category safe URL"),
        help_text=("format: required, letters, numbers, underscore, or hyphens"),
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(
        auto_now=True,
        help_text=("format: Y-m-d H:M:S"),
    )

    class Meta:
        """Meta definition for NewsCategory."""

        ordering = ("-date_created",)
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name


class PostNewsObjects(models.Manager):
    """
    CUSTOM POST OBJECTS MANAGER
    """

    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class PostNews(models.Model):
    """Model definition for PostNews."""

    id=models.UUIDField(primary_key=True,default=uuid4)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=("Author"))
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.DO_NOTHING,
        verbose_name=("News Category"),
    )
    title = models.CharField(max_length=255)
    content = HTMLField()
    source = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=("News source"),
        help_text=("format: it could be links or person name"),
    )    
    options = (("draft", "Draft"), ("published", "Published"))
    status = models.CharField(max_length=50, choices=options, default="published")
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        max_length=255,
        unique_for_date="date_created",
        verbose_name=("url link related to title"),
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        help_text=("format: Y-m-d H:M:S"),
    )
    objects = models.Manager()
    postnewsobjects = PostNewsObjects()

    class Meta:
        """Meta definition for PostNews."""

        ordering = ("-date_created",)
        verbose_name = "Post News"
        verbose_name_plural = "Post News"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newspostdetail", kwargs={"slug": self.slug, "id": self.id})


class PostNewsMedia(models.Model):
    """Model definition for PostNewsMedia."""

    id=models.UUIDField(primary_key=True,default=uuid4)
    postnews = models.ForeignKey(PostNews, on_delete=models.DO_NOTHING)
    images = models.ImageField(
        upload_to="posts/news",
        null=True,
        blank=True,
        help_text=("format: optional,not neccessary to upload pics"),
    )
    file = models.FileField(
        upload_to="posts/files",
        verbose_name=("videos/audio/docs/pdf"),
        null=True,
        blank=True,
        help_text=("format: optional,not neccessary to upload"),
    )
    alt_text = models.CharField(
        max_length=255,
        verbose_name=("alternative text"),
        help_text=("format: required, max-255"),
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name=("Post News display image/files"),
        help_text=("format: default=false, true=default image"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=("post news visibility"),
        help_text=("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=("date post news created"),
        help_text=("format: Y-m-d H:M:S"),
    )

    class Meta:
        """Meta definition for PostNewsMedia."""

        verbose_name = "Post News Media"
        verbose_name_plural = "Post News Media"

    def __str__(self):
        return self.alt_text
