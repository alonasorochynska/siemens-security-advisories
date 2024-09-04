from django.urls import path

from product_CVE.views import (
    index,
    ProductListView,
    VulnerabilityListView,
    SourceURLListView,
    ProductDetailView,
    VulnerabilityDetailView,
    get_cvss_details,
    get_all_vectors,
    CVSSSearchListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("vulnerabilities/", VulnerabilityListView.as_view(), name="vulnerability_list"),
    path("vulnerability/<int:pk>/", VulnerabilityDetailView.as_view(), name="vulnerability_detail"),
    path("documents/", SourceURLListView.as_view(), name="source_url_list"),
    path("get_cvss_details/", get_cvss_details, name="get_cvss_details"),
    path("search_by_cvss/", CVSSSearchListView.as_view(), name="search_by_cvss"),
    path("get_all_vectors/", get_all_vectors, name="get_vulnerabilities_details"),
]

app_name = "product_CVE"
