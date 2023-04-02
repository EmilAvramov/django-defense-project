from django.urls import path, include
from .views import ApiSearch

app_name = "api_app"

urlpatterns = [
    path(
        "search/",
        include(
            [
                path(
                    "digimon",
                    include(
                        [
                            path(
                                "", ApiSearch.as_view(), name="search/digimon"
                            ),
                            path(
                                "/<int:id>",
                                ApiSearch.as_view(),
                                name="search/digimon_by_id",
                            ),
                        ]
                    ),
                ),
                path(
                    "attribute",
                    include(
                        [
                            path(
                                "",
                                ApiSearch.as_view(),
                                name="search/attribute",
                            ),
                            path(
                                "/<int:id>",
                                ApiSearch.as_view(),
                                name="search/attribute_by_id",
                            ),
                        ]
                    ),
                ),
                path(
                    "field",
                    include(
                        [
                            path("", ApiSearch.as_view(), name="search/field"),
                            path(
                                "/<int:id>",
                                ApiSearch.as_view(),
                                name="search/field_by_id",
                            ),
                        ]
                    ),
                ),
                path(
                    "level",
                    include(
                        [
                            path("", ApiSearch.as_view(), name="search/level"),
                            path(
                                "/<int:id>",
                                ApiSearch.as_view(),
                                name="search/level_by_id",
                            ),
                        ]
                    ),
                ),
                path(
                    "type",
                    include(
                        [
                            path("", ApiSearch.as_view(), name="search/type"),
                            path(
                                "/<int:id>",
                                ApiSearch.as_view(),
                                name="search/type_by_id",
                            ),
                        ]
                    ),
                ),
                path(
                    "skill",
                    include(
                        [
                            path("", ApiSearch.as_view(), name="search/skill"),
                            path(
                                "/<int:id>",
                                ApiSearch.as_view(),
                                name="search/skill_by_id",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )
]
