from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50)
    version_range = models.CharField(max_length=255, blank=True, null=True)
    support_url = models.URLField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    remediation_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.product_id})"


class Vulnerability(models.Model):
    cve = models.CharField(max_length=20)
    cwe_id = models.CharField(max_length=20)
    cwe_name = models.CharField(max_length=255)
    summary = models.TextField()
    products = models.ManyToManyField(Product, related_name="vulnerability_products")
    base_score = models.FloatField()
    base_severity = models.CharField(max_length=50)
    vector_string = models.CharField(max_length=255)
    cvss_version = models.CharField(max_length=10)
