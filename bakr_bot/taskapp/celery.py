import os
from celery import Celery
from celery.schedules import crontab
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.local"
    )  # pragma: no cover


app = Celery("bakr_bot")
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


class CeleryAppConfig(AppConfig):
    name = "bakr_bot.taskapp"
    verbose_name = "Celery Config"

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        app.conf.beat_schedule = {
            'run-get-supported-leagues-matches-every-day-at-12-am': {
                'task': 'bakr_bot.football.tasks.get_supported_leagues_matches',
                'schedule': crontab(
                    minute=settings.TASK_GET_LEAGUES_MATCHES_RUNTIME_MINUTE,
                    hour=settings.TASK_GET_LEAGUES_MATCHES_RUNTIME_HOUR, day_of_week='*',
                    day_of_month='*', month_of_year='*'
                ),  # Run daily at 12 AM server time (UTC); 2 AM Cairo; 1 AM London;
            },
        }


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover
