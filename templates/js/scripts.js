document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('uploadForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const clickedButton = event.submitter.id;

        if (clickedButton === "formBtnSubmit") {
            const formData = new FormData(form);

            fetch('/convert', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(html => {
                document.open();
                document.write(html);
                document.close();
            })
            .catch(error => console.error("Error:", error));
        }
    });
});
