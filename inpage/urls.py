from django.urls import path
from inpage import views

from .views import ZipFileView

urlpatterns = [
    path('', views.index, name='index'),
    path('massupload/vk/', views.massupload_vk, name='massupload_vk'),
    path(
        'massupload/instagram/',
        views.massupload_inst,
        name='massupload_inst'
    ),
    path(
        'massupload/whatsapp/',
        views.massupload_whatsapp,
        name='massupload_whatsapp'
    ),
    path('massupload/ok/', views.massupload_ok, name='massupload_ok'),
    path('massupload/tg/', views.massupload_tg, name='massupload_tg'),
    path('upload/vk/', views.upload_vk, name='upload_vk'),
    path('upload/tg/', views.upload_tg, name='upload_tg'),
    path('upload/ok/', views.upload_ok, name='upload_ok'),
    path('upload/inst/', views.upload_inst, name='upload_inst'),
    path('upload/whatsapp/', views.upload_whatsapp, name='upload_whatsapp'),
    path('check-accounts/', ZipFileView.as_view(), name='check-accounts'),
    path('report/', views.report, name='report'),
    path('contacts/', views.contacts, name='contacts'),
    path('useragreements/', views.user_agreements, name='user_agreements'),
]
