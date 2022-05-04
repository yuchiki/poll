"""
admin 設定を管理するモジュール
"""

from django.contrib import admin
from .models import Question

admin.site.register(Question)
