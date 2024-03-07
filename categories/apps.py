from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "categories"

    def ready(self) -> None:

        from . import signals

        return super().ready()
