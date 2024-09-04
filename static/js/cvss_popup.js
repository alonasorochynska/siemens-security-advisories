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


document.getElementById("closePopup").onclick = function() {
    document.getElementById("detailsPopup").style.display = "none";
};
