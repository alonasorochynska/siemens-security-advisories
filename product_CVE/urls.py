from django.urls import path

from product_CVE.views import index, ProductListView, VulnerabilityListView, SourceURLListView, ProductDetailView

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("vulnerabilities/", VulnerabilityListView.as_view(), name="vulnerability_list"),
    path("documents/", SourceURLListView.as_view(), name="source_url_list"),
]

app_name = "product_CVE"
