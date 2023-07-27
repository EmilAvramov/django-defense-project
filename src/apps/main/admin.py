from django.contrib import admin
from .models import (
    Digimon
)


@admin.register(Digimon)
class DigimonAdmin(admin.ModelAdmin):
    list_display = ("name", "antibody", "release_date")

    list_filter = (
        "antibody",
        "release_date",
        "levels__level_name",
        "attributes__attr_name",
        "fields__field_name",
    )

    search_fields = (
        "name",
        "descriptions__origin",
        "descriptions__language",
        "skills__skill_name",
    )

    fieldsets = (
        (None, {"fields": ("name", "antibody", "release_date")}),
        ("Images", {"fields": ("images", "comments")}),
        ("Attributes", {"fields": ("attributes",)}),
        ("Levels and Skills", {"fields": ("levels", "skills")}),
        ("Evolutions", {"fields": ("prior_evos", "next_evos")}),
    )

    raw_id_fields = (
        "images",
        "levels",
        "attributes",
        "fields",
        "descriptions",
        "skills",
        "prior_evos",
        "next_evos",
    )

    save_on_top = True

    related_search_fields = {
        "descriptions": ("origin", "language"),
        "skills": ("skill_name", "translation"),
        "prior_evos": ("evo_name",),
        "next_evos": ("evo_name",),
    }
