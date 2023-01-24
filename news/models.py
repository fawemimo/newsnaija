from django.db import models
from accounts.models import User
from django.urls import reverse
from uuid import uuid4
from tinymce.models import HTMLField
from django.utils.text import slugify
# from taggit.managers import TaggableManager

class NewsCategory(models.Model):
    """Model definition for NewsCategory."""

    id=models.UUIDField(primary_key=True,default=uuid4)
    name = models.CharField(verbose_name="Category name", max_length=255)
    slug = models.SlugField(
        max_length=255,
        verbose_name=("category safe URL"),
        help_text=("format: required, letters, numbers, underscore, or hyphens"),
    )
    seo_title = models.CharField(max_length=255,default='')
    seo_descriptions = models.TextField(default='')
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
        verbose_name = "Article Category"
        verbose_name_plural = "Articles Categories"

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("newspostdetail")    

class Tag(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    name = models.CharField(verbose_name="Tag name", max_length=25, unique=True)   
    slug = models.SlugField(verbose_name='URL related name',blank=True,null=True) 


    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("postnewstag", kwargs={"slug": self.slug})


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
    tag = models.ManyToManyField(Tag, help_text=("You can select more than one options"))  
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
        
    )
    seo_title = models.CharField(max_length=255,default='')
    seo_descriptions = models.TextField(default='')
    date_updated = models.DateTimeField(
        auto_now=True,
        help_text=("format: Y-m-d H:M:S"),
    )
    objects = models.Manager()
    postnewsobjects = PostNewsObjects()

    class Meta:
        """Meta definition for PostNews."""

        ordering = ("-date_created",)
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.description[:150] + ' ...'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(PostNews, self).save(args, kwargs)    

    def get_absolute_url(self):
        return reverse("newspostdetail", kwargs={"slug": self.slug})


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
    media_file = models.FileField(
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
        blank=True,
        null=True
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name=("articles visibility as front display image"),
        help_text=("format: default=false, true=default image"),
    )    
    seo_keywords = models.CharField(max_length=255,default='')
    seo_image = models.ImageField(upload_to="seo/images", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=("date articles created"),
        help_text=("format: Y-m-d H:M:S"),
    )

    class Meta:
        """Meta definition for PostNewsMedia."""

        verbose_name = "Article Media"
        verbose_name_plural = "Articles Media"

    def __str__(self):
        return self.alt_text
