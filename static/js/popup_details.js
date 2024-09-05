// Function to show more vectors based on product ID
function showMore(productId) {
    fetch(`/get_all_vectors?product_id=${productId}`)
        .then(response => response.json())
        .then(data => {
            let content = "<ul>";
            data.vulnerabilities.forEach(function(vulnerability) {
                content += `<li>${vulnerability.vector_string}</li>`;
            });
            content += "</ul>";
            document.getElementById("detailsContent").innerHTML = content;
            document.getElementById("detailsPopup").style.display = "block";
        });
}

// Function to show product information based on vulnerability ID
function showProductInfo(vulnerabilityId) {
    fetch(`/get_product_info?vulnerability_id=${vulnerabilityId}`)
        .then(response => response.json())
        .then(data => {
            let content = "<ul>";
            data.products.forEach(function(product) {
                content += `<li><a href="/product/${product.id}">${product.name}</a></li>`;
            });
            content += "</ul>";
            document.getElementById("detailsContent").innerHTML = content;
            document.getElementById("cvssTitle").textContent = "Product Information";
            document.getElementById("detailsPopup").style.display = "block";
        })
        .catch(error => {
            console.error("Error fetching product info:", error);
        });
}

// Function to show CVSS details based on vector string
function showDetails(vectorString) {
    fetch(`/get_cvss_details?vector_string=${encodeURIComponent(vectorString)}`)
        .then(response => response.json())
        .then(data => {
            let content = "<ul>";
            for (let [key, value] of Object.entries(data)) {
                content += `<li><strong>${key}:</strong> ${value}</li>`;
            }
            content += "</ul>";
            document.getElementById("detailsContent").innerHTML = content;
            document.getElementById("cvssTitle").textContent = "Details: " + vectorString;
            document.getElementById("detailsPopup").style.display = "block";
        });
}

// Function to show CVE information based on product ID
function showCVEInfo(productId) {
    fetch(`/get_cve_info?product_id=${productId}`)
        .then(response => response.json())
        .then(data => {
            let content = "<ul>";
            data.vulnerabilities.forEach(function (vulnerability) {
                content += `<li><a href="/vulnerability/${vulnerability.id}/">${vulnerability.cve}</a></li>`;
            });
            content += "</ul>";
            document.getElementById("detailsContent").innerHTML = content;
            document.getElementById("detailsPopup").style.display = "block";
        })
        .catch(error => {
            console.error("Error fetching CVE info:", error);
        });
}

// Universal function to close popup
function closePopup() {
    document.getElementById("detailsPopup").style.display = "none";
}

// Attach the close event to the close button
document.getElementById("closePopup").onclick = closePopup;
