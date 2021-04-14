# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser

from discount_code import settings
from discount_code.api.base.models import BaseModel
from asgiref.sync import async_to_sync

import datetime
import random


class Client(AbstractUser, BaseModel):
    is_brand = models.BooleanField(default=False)


class Brand(BaseModel):
    brand_name_validator = UnicodeUsernameValidator()
    brand_name = models.CharField(max_length=16, default='', null=True)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Brand_owner', null=True, blank=True,
                                 on_delete=models.CASCADE)


class UserDiscontRelation(BaseModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='UserDiscontRelation_user', null=False,
                                blank=False, on_delete=models.CASCADE)
    discount_id = models.ForeignKey(settings.DISCOUNT_MODEL, related_name='UserDiscontRelation_discount', null=False,
                                    blank=False, on_delete=models.CASCADE)


def __get_randome_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


# ToDo needs to improve to be unique (e.g brand_name + random_code + db_id)
def _generate_discount_code():
    return __get_randome_code(10)


class DiscountCode(BaseModel):
    value = models.CharField(max_length=16, null=False,
                             blank=False, default=_generate_discount_code)
    discount_percent = models.IntegerField(default=0)
    expired_at = models.DateTimeField(null=False, blank=False)
    valid = models.BooleanField(default=True)
    max_usage = models.IntegerField(default=1)
    brand_id = models.ForeignKey(settings.BRAND_MODEL, related_name='DiscountCode_brand', null=False, blank=False,
                                 on_delete=models.CASCADE)

    def can_create_by(self, user):
        return user.is_brand or user.is_superuser

    def can_read_by(self, user):
        return True

    def can_update_by(self, user):
        return user.is_brand or user.is_superuser

    def can_delete_by(self, user):
        return user.is_brand or user.is_superuser

    @classmethod
    def limit_queryset(cls, queryset, user: Client, ):
        # ToDo You can use select_related for optimization if necessary
        result = cls.limit_query_set(queryset, user)

        if not hasattr(user, 'is_brand'):
            try:
                user = Client.objects.get(username=user.username)
            except Client.DoesNotExist:
                return result

        if user.is_superuser:
            result = queryset
        elif user.is_brand:
            result = queryset.filter(brand_id__owner_id=user.id)
        else:
            # current_date = datetime.datetime.now() - datetime.timedelta(days=1)
            current_date = datetime.datetime.now()
            result = queryset.filter(
                valid=True, expired_at__lt=current_date, UserDiscontRelation_discount__user_id=user.id)
        return result
