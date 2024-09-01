from django.shortcuts import render
from django.views.generic import ListView

from product_CVE.models import Product, Vulnerability


def index(request):
    return render(request, "index.html")


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


class VulnerabilityListView(ListView):
    model = Vulnerability
    template_name = "vulnerabilities/vulnerability_list.html"
    context_object_name = "vulnerabilities"
