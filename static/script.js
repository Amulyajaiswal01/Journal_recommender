function uploadPDF() {
    const fileInput = document.getElementById("pdfUpload");
    if (fileInput.files.length === 0) {
        alert("Please select a PDF file to upload.");
        return;
    }
    
    const formData = new FormData();
    formData.append("pdf", fileInput.files[0]);
    
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        displayRecommendations(data);
    })
    .catch(error => console.error("Error:", error));
}

function displayRecommendations(data) {
    const recommendationsDiv = document.getElementById("recommendations");
    recommendationsDiv.innerHTML = "<h2>Recommended Journals</h2>";
    
    if (data.journals.length === 0) {
        recommendationsDiv.innerHTML += "<p>No recommendations found.</p>";
        return;
    }
    
    const list = document.createElement("ul");
    data.journals.forEach(journal => {
        const listItem = document.createElement("li");
        listItem.textContent = journal;
        list.appendChild(listItem);
    });
    recommendationsDiv.appendChild(list);
}
