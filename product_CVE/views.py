from django.shortcuts import render
from django.views.generic import ListView

from product_CVE.models import Product, ProductBranch


def index(request):
    return render(request, "index.html")


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.prefetch_related("product_branches").all()
