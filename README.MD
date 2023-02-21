# Django İHA KİRALAMA PROJESİ
Bu dizin "BAYKAR TEKNOLOJİ" Back-End Developer Vaka Çalışması için oluşturulmuştur.

## Açıklama:
- Ön yüzde Admin-Lte hazır template'ini kullanılmıştır.
- IHA CRUD işlemlerinde Django Rest Framework kullanılmıştır.
- Üyelik ve Giriş ekranlarından django forms kullanılmıştır.
- IHA Filtreleme işlemlerinde django-filters kullanılmıştır.
- Veritabanı olarak postresql kullanılmıştır.
- Jquery ve ajax ile asenkron yapılar kullanılmıştır.
- Çoklu dil için django-rosetta kütüphanesi kullanılmıştır.

## Gereksinimler:
```text
asgiref==3.6.0
certifi==2022.12.7
charset-normalizer==3.0.1
Django==3.2.18
django-cors-headers==3.13.0
django-filter==22.1
django-parler==2.3
django-rosetta==0.9.8
djangorestframework==3.14.0
idna==3.4
polib==1.1.1
psycopg2==2.9.5
python-gettext==4.1
pytz==2022.7.1
requests==2.28.2
sqlparse==0.4.3
typing-extensions==4.5.0
urllib3==1.26.14
```

### 1. Proje sonundaki dizinimiz
```terminal
.
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── iha
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── filters.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── user
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── locale
├── static
├── templates
├── templatetags
├── utils
└── manage.py
```

### 2. Modeller
iha/models.py 
```python
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid

class IHACategory(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class IHA(models.Model):
    creator = models.ForeignKey(User,models.CASCADE)
    mark = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    weight = models.FloatField(default=0,null=True,blank=True)
    category = models.ForeignKey(IHACategory,models.CASCADE,null=True,blank=True)
    slug = models.CharField(max_length=32,null=True,blank=True)
    status = models.BooleanField(default=True)
    date_of_record = models.DateTimeField(null=True,blank=True)
    date_of_update = models.DateTimeField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4()).replace("-","")
        if not self.date_of_record:
            self.date_of_record = datetime.now()
        self.date_of_update = datetime.now()
        super(IHA, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.creator.username}-{self.mark}-{self.model}-{self.weight}"
```

### 3. Serializerlar

iha/api/serializers.py
```python
from rest_framework import serializers
from iha.models import IHA, IHACategory

class IHASerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    creator_name = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = IHA
        fields = ('id',
                  'slug',
                  'date_of_record',
                  'date_of_update',
                  'mark',
                  'model',
                  'weight',
                  'status',
                  'category_name',
                  'creator_name',
                  'creator',
                  'category')
        read_only_fields = ['id','slug','date_of_record','date_of_update']

class IHACategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IHACategory
        fields = ['id','name']
        read_only_fields = ['id']
```

### 4. Örnek Viewslar

4.1 Rest Api Views iha/api/views.py
```python
from rest_framework import status
from rest_framework.response import Response 

from iha.models import IHA, IHACategory
from iha.api.serializers import IHASerializer, IHACategorySerializer
from iha.filters import IHAFilter

#class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class IHAListCreateAPIView(APIView):
    def get(self, request):
        ihas = IHA.objects.all().order_by("-date_of_update")
        ihas = IHAFilter(request.GET, queryset=ihas).qs

        check_active_status = self.request.query_params.get('status',None)
        if check_active_status is not None:
            ihas = ihas.filter(status=check_active_status)

        serializer = IHASerializer(ihas, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = IHASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
...
```

4.2 Page Views iha/views.py
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def DashboardPage(request):
    context = {}
    return render(request, 'dashboard/index.html', context=context)
...
```

### 5. Url endpointlerimiz

5.1 Rest Api Urls iha/api/urls.py

```python
from django.urls import path
from iha.api import views as api_views

urlpatterns = [
    path('',api_views.IHAListCreateAPIView.as_view(), name='api-iha-list'),
    path('<int:pk>', api_views.IHADetailAPIView.as_view(), name='api-iha-detail'),
    path('category/', api_views.IHACategoryListCreateAPIView.as_view(), name='api-iha-category-list'),
]
```

5.2 Page Urls iha/api/urls.py

```python
from django.urls import path
from iha.views import DashboardPage,ihaAddPage,ihaListPage,ihaUpdatePage

urlpatterns = [
    path('', DashboardPage,name='dashboardPage'),
    path('iha/add/', ihaAddPage,name='ihaAddPage'),
    path('iha/list/', ihaListPage,name='ihaListPage'),
    path('iha/update/<id>/', ihaUpdatePage,name='ihaUpdatePage'),
]
```

### 6. Örnek Unit Testlerimiz

iha/tests.py

```python
from django.test import TestCase
from django.urls import reverse
from iha.models import IHA, IHACategory
from django.contrib.auth.models import User


# Create your tests here.


class URLTests(TestCase):
    print("test checking page urls")

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_iha_add(self):
        response = self.client.get("/iha/add/")
        self.assertEqual(response.status_code, 200)

    def test_iha_list(self):
        response = self.client.get("/iha/list/")
        self.assertEqual(response.status_code, 200)
...
```

### 7. Queryset filtreleme için oluşturduğumuz Filter

iha/filters.py

```python
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
```

### 8. Çoklu Dil 
Kullanılan Kütüphaneler

- django-rosetta

Jinja template'de kullanabilmek için bir template tagımız.

8.1 templatetags/i18n_switcher.py
```python
from django import template
from django.template.defaultfilters import stringfilter
from utils.language_functions import switch_lang_code
register = template.Library()


@register.filter
@stringfilter
def switch_i18n_prefix(path, language):
    """takes in a string path"""
    return switch_lang_code(path, language)


@register.filter
def switch_i18n(request, language):
    """takes in a request object and gets the path from it"""
    return switch_lang_code(request.get_full_path(), language)
```

Tetiklendiğinde dili değiştiren fonksiyonumuz

8.2 utils/language_functions.py
```python
from django.conf import settings

def switch_lang_code(path, language):
    # Get the supported language codes
    lang_codes = [c for (c, name) in settings.LANGUAGES]
    # Validate the inputs
    if path == '':
        raise Exception('URL path for language switch is empty')
    elif path[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)
    # Split the parts of the path
    parts = path.split('/')

    # Add or substitute the new language prefix
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language

    # Return the full new path
    return '/'.join(parts)
```

### 9. Jquery ve Ajax ile Crud İşlemi Örneği
```javascript
var request_dict = {
                "mark": mark,
                "model": model,
                "weight": weight,
                "status": status,
                "creator": creator,
                "category": category
            }
var add_url = "{% url 'api-iha-list' %}"

$.ajax({
    method: "POST",
    url: add_url,
    contentType: 'application/json',
    dataType: "text",
    data: JSON.stringify(request_dict)
    }).done(function (res, textStatus, jqXHR) {
            formAddIha[0].reset();
            Swal.fire("{% trans 'Added!' %}", '', 'success')
        }
    );
```

```javascript
var delete_url = "{% url 'api-iha-detail' pk=1 %}".replace(/1/, id.toString());

$.ajax({
    method: "DELETE",
    url: delete_url,
    contentType: 'application/json',
    dataType: 'text',


}).done(function (res, textStatus, jqXHR) {
        if (jqXHR.status === 204) {
            ihatable.row($(element).closest("tr")).remove().draw();
            Swal.fire("{% trans 'Deleted!' %}", '', 'success')
        }
    }
);
```