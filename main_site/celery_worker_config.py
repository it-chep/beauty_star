from appconf import AppConf

__all__ = ["celery_worker"]


class CeleryWorkerConfig(AppConf):
    READINESS_FILE = "/tmp/celery_ready"
    HEARTBEAT_FILE = "/tmp/celery_worker_heartbeat"

    # Настройка проверки воркера
    CHECK_BY_SEC = 1.0
    PRIORITY = 10
    READY_TIME_CONSTRAINT = 60
    LIVENESS_TIME_CONSTRAINT = 60

    class Meta:
        prefix = "celery_worker"


celery_worker_config = CeleryWorkerConfig()
