from rest_framework import serializers
from .models import ProductSimple,ProductMultiple,ProductBulk,ProductConfigurable
from .models import ProductBulkOfMultiple,ProductBulkOfBulk
from .models import ProductMultipleOfBulk,ProductMultipleOfMultiple
from .models import ProductConfigurableOfMultiple,ProductConfigurableOfBulk
from .models import ProductBooleanEav,ProductCharEav,ProductIntEav,ProductTextEav,ProductDecimalEav,ProductUrlEav
from .models import Attribute

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ('company',)
        read_only_fields = ('id',)

class ProductIntEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIntEav
        exclude = ('company','marketplace')
        read_only_fields = ('id',)

class ProductCharEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharEav
        exclude = ('company','marketplace')
        read_only_fields = ('id',)

class ProductBooleanEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBooleanEav
        exclude = ('company','marketplace')
        read_only_fields = ('id',)

class ProductTextEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTextEav
        exclude = ('company','marketplace')
        read_only_fields = ('id',)

class ProductDecimalEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDecimalEav
        exclude = ('company','marketplace')
        read_only_fields = ('id',)

class ProductUrlEavSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductUrlEav
        exclude = ('company','marketplace')
        read_only_fields = ('id',)

class ProductSimpleSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductSimple
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')
        depth=1

class ProductMultipleSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductMultiple
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

class ProductBulkSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductBulk
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

class ProductConfigurableSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductConfigurable
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')


class ProductBulkOfMultipleSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductBulkOfMultiple
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

class ProductBulkOfBulkSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductBulkOfBulk
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

class ProductMultipleOfBulkSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductMultipleOfBulk
        fields = '__all__'
        read_only_fields = ('id','company','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

class ProductMultipleOfMultipleSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductMultipleOfMultiple
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

class ProductConfigurableOfMultipleSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductConfigurableOfMultiple
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

class ProductConfigurableOfBulkSerializer(serializers.ModelSerializer):
    int_eav=ProductIntEavSerializer(many=True)
    boolean_eav=ProductBooleanEavSerializer(many=True)
    char_eav=ProductCharEavSerializer(many=True)
    decimal_eav=ProductDecimalEavSerializer(many=True)
    text_eav=ProductTextEavSerializer(many=True)
    url_eav=ProductUrlEavSerializer(many=True)
    class Meta:
        model = ProductConfigurableOfBulk
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')


