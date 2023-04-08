# from django.contrib.flatpages.admin import FlatPageAdmin
# from tinymce.widgets import TinyMCE
from django.contrib import admin, messages
from django.core.cache import cache
from django.core.paginator import Paginator
from django.utils.html import format_html, urlencode
from django.utils.translation import ngettext

from .models import *


class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:

            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self.__count = cache.get(key, -1)
                if self.__count == -1:
                    self.__count = super().count
                    cache.set(key, self.__count, 3600)

            except:
                self.__count = len(self.object_list)

        return self.__count

    count = property(_get_count)


# class NewsPostsInline(admin.StackedInline):
#     model = PostNews
#     extra = 1


class NewsPostsMediaInline(admin.StackedInline):
    model = PostNewsMedia
    extra = 1


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    """Admin View for NewsCategory"""

    list_display = ("id", "name", "slug")
    list_filter = ("name",)
    readonly_fields = ("id",)
    search_fields = ("name",)
    date_hierarchy = "date_created"
    prepopulated_fields = {"slug": ("name",)}
    # inlines = [NewsPostsInline]
    list_per_page = 25


@admin.register(PostNews)
class PostNewsAdmin(admin.ModelAdmin):
    """Admin View for PostNews"""

    #  custom actions on the news list posts to update to published
    def status_published(self, request, queryset):
        published = queryset.update(status="published")

        #  return messages output
        self.message_user(
            request,
            ngettext(
                "%d articles was successfully updated to published.",
                "%d articles were successfully updated as published.",
                published,
            )
            % published,
            messages.SUCCESS,
        )

    # custom actions on the articles list posts to update to draft
    def status_draft(self, request, queryset):
        draft = queryset.update(status="draft")

        #  return messages output
        self.message_user(
            request,
            ngettext(
                "%d articles was successfully updated to draft.",
                "%d articles were successfully updated as draft.",
                draft,
            )
            % draft,
            messages.SUCCESS,
        )

    # returning individual user post news
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

    # Ordering of the user
    @admin.display(ordering="user__first_name")
    def user_first_name(self, obj):
        return obj.user.first_name

    # overriding the save method
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    #  overriding the form save method
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    date_hierarchy = "date_created"
    list_editable = ("status",)
    list_display = (
        "id",
        "slug",
        "user",
        "category",
        "title",
        "status",
        "date_created",
        "date_updated",
    )

    actions = [status_published, status_draft]

    list_filter = ("status", "date_created", "date_updated")
    search_fields = ("content", "title__iexact", "user__iexact")
    show_full_result_count = False
    paginator = CachingPaginator
    inlines = [NewsPostsMediaInline]
    fieldsets = (
        ("Author", {"fields": ("user",)}),
        ("Select Category", {"fields": ("category",)}),
        (
            "News Post",
            {"fields": ("title", "content", "tag", "seo_title", "seo_descriptions")},
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("status", "slug"),
            },
        ),
    )
    list_select_related = (
        "user",
        "category",
    )
    autocomplete_fields = ["user", "category", "tag"]
    list_per_page = 25
    prepopulated_fields = {"slug": ("title",)}

    # readonly_fields = ("id",)


@admin.register(PostNewsMedia)
class PostNewsMediaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = User.objects.get(id=request.user.id)
        media = PostNewsMedia.objects.filter(postnews__user=user)
        if user.is_superuser:
            return queryset
        else:
            return media

    def thumbnail(self, instance):
        if instance.images.name != "":
            return format_html(f'<img src="{instance.images.url}" class="thumbnail"/>')

    class Media:
        css = {"all": ["news/styles.css"]}

    list_display = ("postnews", "thumbnail", "is_feature", "created_at", "updated_at")

    list_filter = ["is_feature", "created_at"]
    search_fields = ["alt_text", "postnews__title"]
    list_select_related = ["postnews"]
    list_per_page = 25


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    search_fields = ["name"]
    list_per_page = 25
    prepopulated_fields = {"slug": ("name",)}
