from django.db import models


class Publisher(models.Model):
    category = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    namespace = models.URLField()


class Reference(models.Model):
    category = models.CharField(max_length=100)
    summary = models.CharField(max_length=255)
    url = models.URLField()


class RevisionHistory(models.Model):
    date = models.DateTimeField()
    legacy_version = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    summary = models.TextField()


class Tracking(models.Model):
    current_release_date = models.DateTimeField()
    generator_name = models.CharField(max_length=255)
    generator_version = models.CharField(max_length=50)
    tracking_id = models.CharField(max_length=100)
    initial_release_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    version = models.CharField(max_length=10)
    revision_history = models.ManyToManyField(RevisionHistory, related_name="tracking_histories")


class Note(models.Model):
    category = models.CharField(max_length=100)
    text = models.TextField()
    title = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50)
    version_range = models.CharField(max_length=255, blank=True, null=True)


class ProductBranch(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name="product_branches")


class Vulnerability(models.Model):
    cve = models.CharField(max_length=20)
    cwe_id = models.CharField(max_length=20)
    cwe_name = models.CharField(max_length=255)
    summary = models.TextField()
    product_status = models.ManyToManyField(Product, related_name="vulnerability_products")
    mitigation_details = models.TextField()
    no_fix_planned_details = models.TextField(blank=True, null=True)
    vendor_fix_details = models.TextField(blank=True, null=True)
    base_score = models.FloatField()
    base_severity = models.CharField(max_length=50)
    vector_string = models.CharField(max_length=255)
    cvss_version = models.CharField(max_length=10)


class Document(models.Model):
    category = models.CharField(max_length=100)
    csaf_version = models.CharField(max_length=10)
    distribution_text = models.CharField(max_length=255)
    tlp_label = models.CharField(max_length=50)
    lang = models.CharField(max_length=10)
    notes = models.ManyToManyField(Note, related_name="document_notes")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="document_publishers")
    references = models.ManyToManyField(Reference, related_name="document_references")
    title = models.CharField(max_length=255)
    tracking = models.OneToOneField(Tracking, on_delete=models.CASCADE, related_name="document_tracking")
    vulnerabilities = models.ManyToManyField(Vulnerability, related_name="document_vulnerabilities")
    source_url = models.URLField()


class ProductTree(models.Model):
    branches = models.ManyToManyField(ProductBranch, related_name="product_tree_branches")
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="product_tree_document")
