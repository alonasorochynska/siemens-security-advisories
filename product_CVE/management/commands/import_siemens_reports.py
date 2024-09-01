import json
from django.core.management.base import BaseCommand
from product_CVE.models import Product, Vulnerability

class Command(BaseCommand):
    help = "Load Siemens reports data from JSON file into the database"

    def handle(self, *args, **kwargs):
        with open("scraper/data/siemens_reports_one.json", encoding="utf-8") as f:
            data_list = json.load(f)

        for data in data_list:

            # Load Products data
            current_products = {}
            for vendor_branch in data["product_tree"]["branches"]:
                for product_branch_data in vendor_branch.get("branches", []):
                    for version_branch in product_branch_data.get("branches", []):
                        product_data = version_branch["product"]
                        product = Product.objects.create(
                            name=product_data["name"],
                            product_id=product_data["product_id"],
                            version_range=version_branch.get("name", ""),
                        )
                        current_products[product.product_id] = product

            # Extract URLs from remediations and assign to products
            for vulnerability_data in data["vulnerabilities"]:
                for remediation in vulnerability_data.get("remediations", []):
                    url = remediation.get("url")
                    if url:
                        for product_id in remediation["product_ids"]:
                            product = current_products.get(product_id)
                            if product:
                                product.url = url
                                product.save()

            # Load Vulnerabilities data (create new records)
            vulnerabilities = []
            for vulnerability_data in data["vulnerabilities"]:
                score_data = vulnerability_data.get("scores", [{}])[0].get("cvss_v3", {})
                base_score = score_data.get("baseScore", "")
                base_severity = score_data.get("baseSeverity", "")
                vector_string = score_data.get("vectorString", "")
                cvss_version = score_data.get("version", "")
                summary = vulnerability_data["notes"][0]["text"]

                vulnerability = Vulnerability.objects.create(
                    cve=vulnerability_data["cve"],
                    cwe_id=vulnerability_data["cwe"]["id"],
                    cwe_name=vulnerability_data["cwe"]["name"],
                    summary=summary,
                    base_score=base_score,
                    base_severity=base_severity,
                    vector_string=vector_string,
                    cvss_version=cvss_version,
                )
                vulnerabilities.append(vulnerability)

            affected_products_ids = data["vulnerabilities"][0]["product_status"]["known_affected"]
            for vulnerability in vulnerabilities:
                for product_id in affected_products_ids:
                    product = current_products.get(product_id)
                    if product:
                        vulnerability.products.add(product)

        self.stdout.write(
            self.style.SUCCESS("Data successfully loaded into the database.")
        )
