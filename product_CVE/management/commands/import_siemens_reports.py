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
                            source_url=data["document"].get("source_url", "")
                        )
                        current_products[product.product_id] = product

            # Load Vulnerabilities data and assign URLs and remediation details to products
            vulnerabilities = []
            for vulnerability_data in data["vulnerabilities"]:
                score_data = vulnerability_data.get("scores", [{}])[0].get("cvss_v3", {})

                vulnerability = Vulnerability.objects.create(
                    cve=vulnerability_data["cve"],
                    cwe_id=vulnerability_data["cwe"]["id"],
                    cwe_name=vulnerability_data["cwe"]["name"],
                    summary=vulnerability_data["notes"][0]["text"],
                    base_score=score_data.get("baseScore", ""),
                    base_severity=score_data.get("baseSeverity", ""),
                    vector_string=score_data.get("vectorString", ""),
                    cvss_version=score_data.get("version", "")
                )
                vulnerabilities.append(vulnerability)

                for remediation in vulnerability_data.get("remediations", []):
                    details = remediation.get("details")
                    url = remediation.get("url")

                    if details:
                        for product_id in remediation["product_ids"]:
                            product = current_products.get(product_id)
                            if product:
                                if product.remediation_details:
                                    product.remediation_details += f"; {details}"
                                else:
                                    product.remediation_details = details
                                if url:
                                    product.support_url = url
                                product.save()

                affected_products_ids = vulnerability_data["product_status"]["known_affected"]
                for product_id in affected_products_ids:
                    product = current_products.get(product_id)
                    if product:
                        vulnerability.products.add(product)

        self.stdout.write(
            self.style.SUCCESS("Data successfully loaded into the database.")
        )
