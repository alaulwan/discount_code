# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# ToDo: Auth, TokenAuth
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from discount_code.api.base.views import BaseViewSet
from discount_code.api.discount_code.serializers import DiscountSerializer, BatchSerializer
from discount_code.api.discount_code.models import DiscountCode
from discount_code.api.discount_code.models import Brand
from discount_code.api.discount_code.models import UserDiscontRelation

import datetime


# @csrf_exempt
class DiscountCodeView(BaseViewSet):
    """
    retrieve: Get a single discount

    list: Get a list of discount codes

    batch_create: Create X discount codes in one call

    user_discount_code: If the user has already one assigned discount code or more for the given brand, they will be returned in a list.
                        else If the user has no assigned discount code, the function will try to find a free discount code for the given brand, and assign it to the user.
                        else If there is no free discount code, the response will be 404.
    """
    serializer_class = DiscountSerializer
    filterset_fields = ('brand__first_name')

    user_response = openapi.Response('List of discout codes', DiscountSerializer(many=True))

    @swagger_auto_schema(methods=['post'], request_body=BatchSerializer, responses={201: user_response})
    @action(methods=['POST', ], detail=False)
    def batch_create(self, request, brand=None):
        request_data = request.data
        serializer = BatchSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        count = request_data.get("count")
        discount_percent = request_data.get("discount_percent")
        expired_at = request_data.get("expired_at")
        brand_name = request_data.get("brand_name")
        if not (count and discount_percent and expired_at and brand_name):
            return Response(
                "Error: somr data are missing. You have to provide count, discount_percent, expired_at and brand_name",
                status=status.HTTP_404_NOT_FOUND)

        try:
            brand = Brand.objects.get(brand_name=brand_name)
        except Brand.DoesNotExist:
            return Response("Error: the brand is not registered in the system.", status=status.HTTP_404_NOT_FOUND)

        data = []
        for i in range(count):
            discount = {
                "discount_percent": discount_percent,
                "expired_at": expired_at,
                "valid": True,
                "max_usage": 1,
                "brand_id": brand.id
            }
            data.append(discount)

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    brand_param_config = openapi.Parameter('brand', in_=openapi.IN_QUERY, description='Brand name',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[brand_param_config])
    @action(methods=['GET', ], detail=False)
    def user_discount_code(self, request, brand=None, ):
        query_params = request.query_params
        brand_name = query_params.get("brand")
        brand = Brand.objects.get(brand_name=brand_name)
        current_date = datetime.datetime.now()
        discount_code_set = DiscountCode.objects.filter(brand_id=brand.id, expired_at__lt=current_date, valid=True,
                                                        UserDiscontRelation_discount__user_id=request.user.id)

        if len(discount_code_set) > 0:
            serializer = self.get_serializer(data=discount_code_set, many=True)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)

        discount_code_set = DiscountCode.objects.filter(brand_id=brand.id, expired_at__lt=current_date, valid=True,
                                                        UserDiscontRelation_discount=None)
        if (len(discount_code_set) > 0):
            discount_code = discount_code_set[0]
            user_discont_relation = UserDiscontRelation.objects.create(user_id=request.user, discount_id=discount_code)
            # user_discont_relation = UserDiscontRelation(user_id=request.user, discount_id=discount_code)
            # user_discont_relation.save()

            serializer = self.get_serializer(data=discount_code_set, many=True)
            serializer.is_valid()
            send_notification(serializer.data[0], request.user)
            return Response(serializer.data[0], status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_404_NOT_FOUND)


def send_notification(discount_code, user):
    # ToDo: Send notification to an endpoint (or maybe to a SQS or Kafka queue)
    pass
