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
    path("vendor/", views.vendor_index, name="vendor_index"),
    path("vendor/create/", views.vendor_create, name="vendor_create"),
    path("vendor/edit/<pk>/", views.vendor_edit, name="vendor_edit"),
    path("vendor/data/<vendor_pk>", views.vendor_data, name="vendor_data"),
]
