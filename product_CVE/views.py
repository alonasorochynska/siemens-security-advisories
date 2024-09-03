from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from product_CVE.forms import ProductSearchForm, VulnerabilitySearchForm
from product_CVE.models import Product, Vulnerability


def index(request):
    product_count = Product.objects.count()
    vulnerability_count = Vulnerability.objects.count()
    average_cvss_score = Vulnerability.objects.aggregate(Avg("base_score"))["base_score__avg"]
    critical_severity_vulnerabilities_count = Vulnerability.objects.filter(base_severity="CRITICAL").count()
    high_severity_vulnerabilities_count = Vulnerability.objects.filter(base_severity="HIGH").count()
    medium_severity_vulnerabilities_count = Vulnerability.objects.filter(base_severity="MEDIUM").count()
    low_severity_vulnerabilities_count = Vulnerability.objects.filter(base_severity="LOW").count()

    context = {
        "product_count": product_count,
        "vulnerability_count": vulnerability_count,
        "average_cvss_score": average_cvss_score,
        "critical_severity_vulnerabilities_count": critical_severity_vulnerabilities_count,
        "high_severity_vulnerabilities_count": high_severity_vulnerabilities_count,
        "medium_severity_vulnerabilities_count": medium_severity_vulnerabilities_count,
        "low_severity_vulnerabilities_count": low_severity_vulnerabilities_count,
    }
    return render(request, "index.html", context)


class ProductListView(ListView):
    model = Product
    template_name = "product_CVE/product_list.html"
    context_object_name = "products"
    queryset = Product.objects.prefetch_related("vulnerability_products").all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_name = self.request.GET.get("product", "")
        context["search_form"] = ProductSearchForm(initial={"product": product_name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductSearchForm(self.request.GET)
        if form.is_valid():
            product_name = form.cleaned_data["product"]
            if product_name:
                queryset = queryset.filter(name__icontains=product_name)
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_CVE/product_detail.html"
    context_object_name = "product"


class VulnerabilityListView(ListView):
    model = Vulnerability
    template_name = "product_CVE/vulnerability_list.html"
    context_object_name = "vulnerabilities"
    queryset = Vulnerability.objects.prefetch_related("products").all()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = VulnerabilitySearchForm(self.request.GET)
        context["search_form"] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VulnerabilitySearchForm(self.request.GET)

        if form.is_valid():
            cve = form.cleaned_data.get("cve")
            severity = form.cleaned_data.get("severity")
            cvss_score = form.cleaned_data.get("cvss_score")

            if cve:
                queryset = queryset.filter(cve__icontains=cve)

            if severity:
                queryset = queryset.filter(base_severity=severity)

            if cvss_score is not None:
                if cvss_score.is_integer():
                    queryset = queryset.filter(base_score__gte=cvss_score, base_score__lt=cvss_score + 1)
                else:
                    queryset = queryset.filter(base_score=cvss_score)

        return queryset


class SourceURLListView(ListView):
    template_name = "product_CVE/source_url_list.html"
    context_object_name = "source_urls"

    def get_queryset(self):
        return Product.objects.values("source_url").distinct()
