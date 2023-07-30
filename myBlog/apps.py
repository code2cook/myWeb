from django.apps import AppConfig


class MyblogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myBlog"

class MyblogUserConfig(AppConfig):
    name = 'myBlog'

    def ready(self):
        import myBlog.signals