# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework import mixins
from rest_framework import viewsets
# from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from discount_code.api.base.permissions import BasePermission


class BaseGenericView(viewsets.GenericViewSet):
    lookup_fields = 'id'
    permission_classes = (IsAuthenticated, BasePermission,)

    def get_queryset(self):
        serializer_class = self.get_serializer_class()
        model = serializer_class.Meta.model
        queryset = model.objects.all()
        limited_queryset = model.limit_queryset(queryset, self.request.user, )
        return limited_queryset


class BaseViewSet(BaseGenericView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  ):
    # authentication_classes = (BasicAuthentication,)
    pass
