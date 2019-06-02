from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "bakr_bot.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import bakr_bot.users.signals  # noqa F401
        except ImportError:
            pass
