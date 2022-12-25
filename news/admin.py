from django.contrib import admin
from .models import *

# from django.contrib.flatpages.admin import FlatPageAdmin
# from tinymce.widgets import TinyMCE
from django.contrib import messages
from django.utils.translation import ngettext

admin.site.register(PostNewsMedia)

class NewsPostsInline(admin.StackedInline):
    model = PostNews
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
    inlines = [NewsPostsInline]


# TINY MCE CUSTOMIZATION
# class TinyMCEFlatPageAdmin(FlatPageAdmin):
#     def formfield_for_dbfield(self, db_field, **kwargs):
#         if db_field.name == 'content':
#             return db_field.formfield(widget=TinyMCE(
#                 attrs={'cols': 80, 'rows': 30},
#                 mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
#             ))
#         return super().formfield_for_dbfield(db_field, **kwargs)


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
                "%d news was successfully updated to published.",
                "%d news were successfully updated as published.",
                published,
            )
            % published,
            messages.SUCCESS,
        )

    # custom actions on the news list posts to update to draft
    def status_draft(self, request, queryset):
        draft = queryset.update(status="draft")

        #  return messages output
        self.message_user(
            request,
            ngettext(
                "%d news was successfully updated to draft.",
                "%d news were successfully updated as draft.",
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
    show_full_result_count = True

    fieldsets = (
        ("Author", {"fields": ("user",)}),
        ("Select Category", {"fields": ("category",)}),
        (
            "News Post",
            {
                "fields": (
                    "title",
                    "content",
                )
            },
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
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 25
