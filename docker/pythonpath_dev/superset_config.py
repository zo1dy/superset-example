import logging
import os
from datetime import timedelta
from typing import Optional

from cachelib.file import FileSystemCache
from celery.schedules import crontab

logger = logging.getLogger()

def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)

# GENERAL
APP_NAME = "APP_NAME"
APP_ICON = "/static/assets/images/superset-logo-horiz.png"
LOGO_TARGET_PATH = None
LOGO_TOOLTIP = "LOGO_TOOLTIP"
LOGO_RIGHT_TEXT = "LOGO_RIGHT_TEXT"
FAB_API_SWAGGER_UI = False
#ROW_LIMIT = 10000
SECRET_KEY = get_env_variable("SECRET_KEY")
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "ru": {"flag": "ru", "name": "Russian"}
}
SIP_15_ENABLED = True
#ENABLE_PROXY_FIX = True
CONTENT_SECURITY_POLICY_WARNING = False

# EMAIL
SMTP_HOST = get_env_variable("SMTP_HOST")
SMTP_PORT = get_env_variable("SMTP_PORT")
SMTP_STARTTLS = False
SMTP_SSL_SERVER_AUTH = False
SMTP_SSL = False
SMTP_USER = ""
SMTP_PASSWORD = ""
SMTP_MAIL_FROM = get_env_variable("SMTP_MAIL_FROM")
EMAIL_REPORTS_SUBJECT_PREFIX = get_env_variable("EMAIL_REPORTS_SUBJECT_PREFIX")

# DATABASE
DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)
# CACHE
REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")
REDIS_FILTERS_DB = get_env_variable("REDIS_FILTERS_DB", "2")
CACHE_DEFAULT_TIMEOUT=get_env_variable("CACHE_DEFAULT_TIMEOUT", 86400)
CACHE_REDIS_URL=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_FILTERS_DB}"
RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")
# Dashboard filter state (required)
FILTER_STATE_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT,
    "CACHE_KEY_PREFIX": "filter_",
    "CACHE_REDIS_URL": CACHE_REDIS_URL
}
# Explore chart form data (required)
EXPLORE_FORM_DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT,
    "CACHE_KEY_PREFIX": "forms_",
    "CACHE_REDIS_URL": CACHE_REDIS_URL
}
# Metadata cache (optional)
FILTER_STATE_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT,
    "CACHE_KEY_PREFIX": "states_",
    "CACHE_REDIS_URL": CACHE_REDIS_URL
}
# Charting data queried from datasets (optional)
DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT,
    "CACHE_KEY_PREFIX": "data_",
    "CACHE_REDIS_URL": CACHE_REDIS_URL
}


# Celery
class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks")
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERYBEAT_SCHEDULE = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }
CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "ENABLE_TEMPLATE_PROCESSING" : True
}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_BASEURL = "http://192.168.36.129:8000/"
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL
SCREENSHOT_LOCATE_WAIT = 100
SCREENSHOT_LOAD_WAIT = 600
SQLLAB_CTAS_NO_LIMIT = True

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
