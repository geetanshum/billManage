from django.urls import path

from . import views
from .views import print_view, statusUpdate

urlpatterns = [
 #path('', views.index, name='index'),
path('', views.subscription, name='subscription'),
 #path('alert/', views.alert, name='alertdata'),
path('subscription/add/', views.addjoinsubscription, name='subscription/add'),
path('report', views.reportbill, name='reportbill'),
path('report/print', print_view ),
path('status/update', statusUpdate)
]
