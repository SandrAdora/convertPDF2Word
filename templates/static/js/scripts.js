document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('uploadForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const clickedButton = event.submitter.id;

        if (clickedButton === "formBtn") {
            // 1. hide main container 
            document.getElementById('main-container').classList.add('hidden');
            // 2. let the loading container appear 
            document.getElementById('loading-container').classList.remove('hidden');
            // 3. Transfer to request to sever 
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
