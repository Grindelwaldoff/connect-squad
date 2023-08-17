"""accmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings

from django.contrib import admin
from django.views.generic import TemplateView

from django.urls import path, include, re_path

from django.conf.urls.static import static, serve


urlpatterns = [

    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),

    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),

    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),

    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('enot_850aa5a9.html', TemplateView.as_view(
        template_name='inpage/enot_850aa5a9.html'
    )),
    path('fk-verify.html', TemplateView.as_view(
        template_name='inpage/fk-verify.html'
    )),
    path('', include(('inpage.urls', 'inpage'), namespace='inpage')),
]


handler404 = 'inpage.views.error_404_view'
handler500 = 'inpage.views.error_view'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
                serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
                serve, {'document_root': settings.STATIC_ROOT}),
    ]
