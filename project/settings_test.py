import os

# Force test-safe values even when the shell already exports production-like env vars.
os.environ["DEBUG"] = "True"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ALLOWED_HOSTS"] = "localhost,127.0.0.1"
os.environ.setdefault("DB_PASSWORD", "postgres")

from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

if "inbound_dashboard" not in INSTALLED_APPS:
    INSTALLED_APPS = [*INSTALLED_APPS, "inbound_dashboard"]

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
