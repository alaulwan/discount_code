from django.conf.urls import url
from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("", views.DiscountCodeView, "discount_code")

urlpatterns = router.urls
