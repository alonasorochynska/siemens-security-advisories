import json
from django.core.management.base import BaseCommand
from product_CVE.models import (
    Publisher,
    Reference,
    RevisionHistory,
    Tracking,
    Note,
    Product,
    ProductBranch,
    Vulnerability,
    Document,
    ProductTree,
)


class Command(BaseCommand):
    help = "Load Siemens reports data from JSON file into the database"

    def handle(self, *args, **kwargs):
        with open("scraper/data/siemens_reports.json", encoding="utf-8") as f:
            data_list = json.load(f)

        for data in data_list:
            # Load Publisher data
            publisher_data = data["document"]["publisher"]
            publisher, created = Publisher.objects.get_or_create(
                category=publisher_data["category"],
                contact_details=publisher_data["contact_details"],
                name=publisher_data["name"],
                namespace=publisher_data["namespace"],
            )

            # Load References data
            references = []
            for ref_data in data["document"]["references"]:
                reference, created = Reference.objects.get_or_create(
                    category=ref_data["category"],
                    summary=ref_data.get("summary", ""),
                    url=ref_data["url"],
                )
                references.append(reference)

            # Load RevisionHistory data
            revision_histories = []
            for rev_data in data["document"]["tracking"]["revision_history"]:
                revision_history, created = RevisionHistory.objects.get_or_create(
                    date=rev_data["date"],
                    legacy_version=rev_data["legacy_version"],
                    number=rev_data["number"],
                    summary=rev_data["summary"],
                )
                revision_histories.append(revision_history)

            # Load Tracking data
            tracking_data = data["document"]["tracking"]
            tracking = Tracking.objects.create(
                current_release_date=tracking_data["current_release_date"],
                generator_name=tracking_data["generator"]["engine"]["name"],
                generator_version=tracking_data["generator"]["engine"]["version"],
                tracking_id=tracking_data["id"],
                initial_release_date=tracking_data["initial_release_date"],
                status=tracking_data["status"],
                version=tracking_data["version"],
            )
            tracking.revision_history.set(revision_histories)

            # Load Notes data
            notes = []
            for note_data in data["document"]["notes"]:
                note, created = Note.objects.get_or_create(
                    category=note_data["category"],
                    text=note_data["text"],
                    title=note_data["title"],
                )
                notes.append(note)

            # Load Products and ProductBranch data
            product_branches = []
            for vendor_branch in data["product_tree"]["branches"]:
                for product_branch_data in vendor_branch.get("branches", []):
                    product_branch, created = ProductBranch.objects.get_or_create(
                        category=product_branch_data["category"],
                        name=product_branch_data["name"],
                    )

                    for version_branch in product_branch_data.get("branches", []):
                        product_data = version_branch["product"]
                        product, created = Product.objects.get_or_create(
                            name=product_data["name"],
                            product_id=product_data["product_id"],
                            version_range=version_branch.get("name", ""),
                        )
                        product_branch.products.add(product)
                    product_branches.append(product_branch)

            # Load Vulnerability data
            vulnerabilities = []
            for vuln_data in data["vulnerabilities"]:
                vulnerability, created = Vulnerability.objects.get_or_create(
                    cve=vuln_data["cve"],
                    cwe_id=vuln_data["cwe"]["id"],
                    cwe_name=vuln_data["cwe"]["name"],
                    summary=vuln_data["notes"][0]["text"],
                    mitigation_details=vuln_data["remediations"][0]["details"],
                    base_score=vuln_data["scores"][0]["cvss_v3"]["baseScore"],
                    base_severity=vuln_data["scores"][0]["cvss_v3"]["baseSeverity"],
                    vector_string=vuln_data["scores"][0]["cvss_v3"]["vectorString"],
                    cvss_version=vuln_data["scores"][0]["cvss_v3"]["version"],
                )
                affected_products = Product.objects.filter(
                    product_id__in=vuln_data["product_status"]["known_affected"]
                )
                vulnerability.product_status.set(affected_products)
                vulnerabilities.append(vulnerability)

            # Load Document data
            document = Document.objects.create(
                category=data["document"]["category"],
                csaf_version=data["document"]["csaf_version"],
                distribution_text=data["document"]["distribution"]["text"],
                tlp_label=data["document"]["distribution"]["tlp"]["label"],
                lang=data["document"]["lang"],
                publisher=publisher,
                tracking=tracking,
                title=data["document"]["title"],
                source_url=data["document"]["source_url"],
            )
            document.notes.set(notes)
            document.references.set(references)
            document.vulnerabilities.set(vulnerabilities)

            # Load ProductTree data
            product_tree = ProductTree.objects.create(document=document)
            product_tree.branches.set(product_branches)

        self.stdout.write(
            self.style.SUCCESS("Data successfully loaded into the database.")
        )
