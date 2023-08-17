from django.urls import path
from shop import views


urlpatterns = [
    path(
        '',
        views.product_list,
        name='product_list'
    ),
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category'
    ),
    path(
        'buy/<int:product_id>/',
        views.buy_product,
        name='buy_product'
    ),
    path(
        'account/detail/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'account/edit/<slug:slug>/',
        views.update_product_detail,
        name='product_update'
    ),
    # path(
    #     'account/delete/<slug:slug>/',
    #     views.product_del,
    #     name='product_delete'
    # )
]
