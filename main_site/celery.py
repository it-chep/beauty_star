import os
import logging
from pathlib import Path

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready, worker_shutdown
from django.conf import settings
from django.utils.module_loading import import_string

from main_site.celery_worker_config import celery_worker_config
from main_site.redis_utils import get_redis

REDIS_CLIENT = get_redis()

logger = logging.getLogger("default")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_star.settings")

app = Celery("beauty_star")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
app.conf.timezone = settings.TIME_ZONE

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_CREATE_MISSING_QUEUES = True
CELERY_BROKER_TRANSPORT = "redis"
CELERY_RESULT_BACKEND = "django-db"


@app.task
def test_task():
    logger.info("Running test_celery task")
    return "echo"


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from django_celery_beat.models import PeriodicTask, PeriodicTasks

    PeriodicTask.objects.update(last_run_at=None)
    unregistered_tasks_ids_by_name = dict(
        PeriodicTask.objects.filter(task__startswith="beauty_star").values_list("task", "id").iterator()
    )
    PeriodicTasks.update_changed()

    sender.add_periodic_task(crontab(minute="*/5"), test_task)

    for app_name, options in settings.CELERY_PERIODICAL_TASKS.items():
        if app_name not in settings.INSTALLED_APPS:
            continue

        for func_name, task_kwargs in options.items():
            func_namespace = f"{app_name}.tasks.{func_name}"
            try:
                task = import_string(func_namespace)
                task_name = task_kwargs.pop("name", func_namespace)
                schedule = task_kwargs.pop("schedule")
                sender.add_periodic_task(schedule, task, name=task_name, kwargs=task_kwargs)
                unregistered_tasks_ids_by_name.pop(func_namespace, None)
                logger.info("Registry periodic task: %s", func_namespace)
            except ImportError:
                logger.warning("Add periodic task import error: %s", func_namespace)
            except Exception as e:
                logger.error("Add periodic task error: %s", e.args[0])

    unregistered_tasks_ids = tuple(unregistered_tasks_ids_by_name.values())
    if unregistered_tasks_ids:
        PeriodicTask.objects.filter(id__in=unregistered_tasks_ids).delete()
        PeriodicTasks.update_changed()
        for task_name in unregistered_tasks_ids_by_name.keys():
            logger.info("Deleted periodic tasks: %s", task_name)


@worker_ready.connect
def worker_ready(**_):
    Path(celery_worker_config.READINESS_FILE).touch()


@worker_shutdown.connect
def worker_shutdown(**_):
    Path(celery_worker_config.READINESS_FILE).unlink(missing_ok=True)
