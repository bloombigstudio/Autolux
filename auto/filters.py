import django_filters
from django.db.models import Q
from django.forms import TextInput, fields
from auto.models import Product

SORT_CHOICES = {
    ('lowToHigh', 'Low to High'),
    ('highToLow', 'High to Low'),
    ('aToz', 'A To Z'),
    ('zToa', 'Z To A'),
}

CATEGORY_CHOICES = {
    ('Interior', 'INTERIOR'),
    ('Exterior', 'EXTERIOR'),
    ('Mats', 'MATS'),
    ('Detailing', 'DETAILING'),
    ('Leds', 'LEDS'),
    ('Suvs', 'SUVS'),
    ('Utilites', 'UTILITES'),
    ('Others', 'OTHERS'),
}

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['product_title', 'product_category', 'product_price']

    # product_title = django_filters.CharFilter(lookup_expr='icontains')
    product_title = django_filters.CharFilter(method='search_filter')
    sorting = django_filters.ChoiceFilter(label="Sort By", choices=SORT_CHOICES, method="filter_by_sort")
    product_category = django_filters.ChoiceFilter(label="Select category", choices=CATEGORY_CHOICES, lookup_expr='iexact')
    product_price = django_filters.RangeFilter()

    def search_filter(self, queryset, name, value):
        queryList = value.split()
        queryList.append(value)
        queries = [Q(product_title__icontains=value) for value in queryList]
        queries1 = [Q(product_title__search=value)]
        query = queries.pop()
        query1 = queries1.pop()
        for item in queries:
            query |= item
        for item1 in queries1:
            query1 |= item1

        intersection = Product.objects.filter(query) & Product.objects.filter(query1)

        return intersection


    def filter_by_sort(self, queryset, name, value):
        if value == 'lowToHigh':
            expression = 'product_price'
        elif value == 'highToLow':
            expression = '-product_price'
        elif value == 'aToz':
            expression = 'product_title'
        elif value == 'zToa':
            expression = '-product_title'

        return queryset.order_by(expression)

    # def filter_by_category(self, queryset, name, value):
    #     return queryset.filter(product_category=value)