# __author__ = "priyanka"

from rest_framework import serializers
from v1.billing.models.rate import Rate as RateTbl
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryListSerializer

class RateShortViewSerializer(serializers.ModelSerializer):
    utility_product_id = UtilityProductShortViewSerializer(source='get_utility_product_name')
    consumer_subcategory_id = ConsumerSubCategoryListSerializer(source='get_consumer_sub_category')
    class Meta:
        model = RateTbl
        fields = ('id_string','rate','unit','utility_product_id','consumer_subcategory_id')