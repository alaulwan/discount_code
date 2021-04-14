from rest_framework import serializers

from discount_code.api.discount_code.models import DiscountCode


class DiscountSerializer(serializers.ModelSerializer):
    brand_name = serializers.PrimaryKeyRelatedField(
        queryset=DiscountCode.objects.all(),
        allow_null=True,
        required=False,
        source='brand_id.brand_name',
    )

    # brand_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = DiscountCode
        fields = (
            "value",
            "discount_percent",
            "expired_at",
            "valid",
            "max_usage",
            "brand_name",
            "brand_id",
            "id"
        )


class BatchSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    discount_percent = serializers.IntegerField()
    expired_at = serializers.DateTimeField()
    brand_name = serializers.CharField(max_length=16)

    class Meta:
        model = DiscountCode
        fields = (
            "count",
            "discount_percent",
            "expired_at",
            "brand_name"
        )
