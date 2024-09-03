from django import forms


class ProductSearchForm(forms.Form):
    product = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name of product"}),
    )


class VulnerabilitySearchForm(forms.Form):
    cve = forms.CharField(
        max_length=20,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by CVE"}),
    )
    severity = forms.ChoiceField(
        choices=[
            ("", "Severity"),
            ("CRITICAL", "Critical"),
            ("HIGH", "High"),
            ("MEDIUM", "Medium"),
            ("LOW", "Low"),
        ],
        required=False,
        label="",
    )
    cvss_score = forms.FloatField(
        required=False,
        label="",
        widget=forms.NumberInput(attrs={
            "placeholder": "CVSS Score", "min": "0", "class": "cvss-score-input"
        }),
    )
