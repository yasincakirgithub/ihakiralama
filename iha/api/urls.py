from django.urls import path
from iha.api import views as api_views

urlpatterns = [
    path('',api_views.IHAListCreateAPIView.as_view(), name='api-iha-list'),
    path('<int:pk>', api_views.IHADetailAPIView.as_view(), name='api-iha-detail'),
    path('category/', api_views.IHACategoryListCreateAPIView.as_view(), name='api-iha-category-list'),
]




