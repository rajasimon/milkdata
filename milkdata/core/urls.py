from django.urls import path

from milkdata.core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shed/entry/", views.shed_entry, name="shed_entry"),
    path("date/", views.date_index, name="date"),
    path("shed/", views.shed_index, name="shed_index"),
    path("shed/create/", views.shed_create, name="shed_create"),
    path(
        "shed_data_create/<shed_name>/", views.shed_data_create, name="shed_data_create"
    ),
    path(
        "shed_data_edit/<shed_data_pk>/",
        views.shed_data_edit,
        name="shed_data_edit",
    ),
    path("distribute/", views.distribute, name="distribute"),
    path("shop/", views.shop_index, name="shop_index"),
    path("shop/create/", views.shop_create, name="shop_create"),
    path("shop/edit/<pk>/", views.shop_edit, name="shop_edit"),
    path("shop/data/<shop_pk>", views.shop_data, name="shop_data"),
]
