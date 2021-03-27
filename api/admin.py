from django.contrib import admin

from api.models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "pk",
        "text",
        "author",
        "score",
        "pub_date",
        "title",
    )
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    """Класс для отображения полей комментария в админке."""

    list_display = (
        "pk",
        "text",
        "author",
        "pub_date",
        "review",
    )
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)