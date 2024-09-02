from django.shortcuts import render
from django.views.generic import ListView, DetailView

from product_CVE.models import Product, Vulnerability


def index(request):
    return render(request, "index.html")


class ProductListView(ListView):
    model = Product
    template_name = "product_CVE/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_CVE/product_detail.html"
    context_object_name = "product"


class VulnerabilityListView(ListView):
    model = Vulnerability
    template_name = "product_CVE/vulnerability_list.html"
    context_object_name = "vulnerabilities"


class SourceURLListView(ListView):
    template_name = "product_CVE/source_url_list.html"
    context_object_name = "source_urls"

    def get_queryset(self):
        return Product.objects.values("source_url").distinct()
