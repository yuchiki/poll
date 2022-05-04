"""polls app の設定ファイル"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """ pollsの設定"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
