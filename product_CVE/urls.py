from django.urls import path

from product_CVE.views import index, ProductListView

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="product_list"),
]

app_name = "product_CVE"
