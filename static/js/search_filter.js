document.addEventListener("DOMContentLoaded", function() {
    const severitySelect = document.querySelector('select[name="severity"]');
    if (severitySelect) {
        severitySelect.onchange = function() {
            this.form.submit();
        };
    }
});
