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

function closePopup() {
    document.getElementById("detailsPopup").style.display = "none";
}
