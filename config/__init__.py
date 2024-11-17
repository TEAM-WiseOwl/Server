from __future__ import absolute_import, unicode_literals

# Celery 앱을 초기화하여 자동으로 작업을 등록합니다.
from .celery import app as celery_app

__all__ = ('celery_app',)