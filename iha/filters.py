import django_filters
from .models import IHA

class IHAFilter(django_filters.FilterSet):

    class Meta:
        model = IHA
        fields = {
            'creator__username':["icontains"],
            'mark':["icontains"],
            'model':["icontains"],
            'weight':["lt","gt"],
            'category__name':["icontains"]
        }