from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from product_CVE.forms import ProductSearchForm, VulnerabilitySearchForm, CVSSSearchForm
from product_CVE.models import Product, Vulnerability
from product_CVE.utils import explain_cvss_vector


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


class VulnerabilityDetailView(DetailView):
    model = Vulnerability
    template_name = "product_CVE/vulnerability_detail.html"
    context_object_name = "vulnerability"


class SourceURLListView(ListView):
    template_name = "product_CVE/source_url_list.html"
    context_object_name = "source_urls"

    def get_queryset(self):
        return Product.objects.values("source_url").distinct()


def get_cvss_details(request):
    vector_string = request.GET.get("vector_string", "")
    if vector_string:
        details = explain_cvss_vector(vector_string)
        return JsonResponse(details)
    return JsonResponse({"error": "Invalid vector string"}, status=400)


class CVSSSearchListView(ListView):
    model = Product
    template_name = "product_CVE/search_by_cvss.html"
    context_object_name = "products"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CVSSSearchForm(self.request.GET or None)
        context["form"] = form
        return context

    def get_queryset(self):
        form = CVSSSearchForm(self.request.GET or None)
        products = []

        if form.is_valid():
            cvss_vector = form.cleaned_data["cvss_vector"]
            vulnerabilities = Vulnerability.objects.filter(
                vector_string__icontains=cvss_vector
            ).prefetch_related("products")

            for vulnerability in vulnerabilities:
                products.extend(vulnerability.products.all())

        return products

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return paginator, page_obj, page_obj.object_list, page_obj.has_other_pages()
