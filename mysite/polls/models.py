"""
pollsのmodels定義モジュール
"""

import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Question は質問のクラス
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        """
        >>> Question("foo", timezone.now() - datetime.timedelta(days=100))
        false

        >>> Question("bar", timezone.now() - datetime.timedelta(minutes=1))
        true
        """

        now = timezone.now()
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    Choice は、質問に対する選択肢です。"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
