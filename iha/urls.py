from django.urls import path
from iha.views import DashboardPage,ihaAddPage,ihaListPage,ihaUpdatePage

urlpatterns = [
    path('', DashboardPage,name='dashboardPage'),
    path('iha/add/', ihaAddPage,name='ihaAddPage'),
    path('iha/list/', ihaListPage,name='ihaListPage'),
    path('iha/update/<id>/', ihaUpdatePage,name='ihaUpdatePage'),
]

