from django.urls import path

from product_CVE.views import index, ProductListView, VulnerabilityListView

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path('vulnerabilities/', VulnerabilityListView.as_view(), name="vulnerability_list"),
]

app_name = "product_CVE"
