from __future__ import unicode_literals

from django.db import models
from django.db.models import QuerySet
from django.utils.timezone import now
from django.contrib.auth.models import User


class LimitedQuerySet(QuerySet):
    def limit_for_user(self, user):
        return self.model.limit_queryset(self, user)


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(default='')

    objects = LimitedQuerySet.as_manager()

    def can_create_by(self, user):
        return False

    def can_read_by(self, user):
        return False

    def can_update_by(self, user):
        return False

    def can_delete_by(self, user):
        return False

    @classmethod
    def limit_query_set(cls, queryset, user):
        return queryset.none()
