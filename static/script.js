// ==========================
// BLITZ - Frontend Script
// ==========================

// Elements
const fileInput = document.getElementById("datasetFile");
const fileName = document.getElementById("fileName");
const targetColumn = document.getElementById("targetColumn");
const algorithm = document.getElementById("algorithm");
const analyzeBtn = document.getElementById("analyzeBtn");
const loading = document.getElementById("loading");
const results = document.getElementById("results");

// ==========================
// File Upload
// ==========================

fileInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    // Show selected filename
    fileName.textContent = file.name;

    // Clear previous target options
    targetColumn.innerHTML =
        '<option value="">Select Target</option>';

    // CSV Header Detection
    if (file.name.toLowerCase().endsWith(".csv")) {

        const reader = new FileReader();

        reader.onload = function (e) {

            const csv = e.target.result;

            const firstLine = csv.split(/\r?\n/)[0];

            // Detect delimiter
            const delimiter = firstLine.includes(";") ? ";" : ",";

            const headers = firstLine.split(delimiter);

            headers.forEach(header => {

                const option = document.createElement("option");

                option.value = header.trim();
                option.textContent = header.trim();

                targetColumn.appendChild(option);

            });

            console.log("Detected Columns:", headers);

        };

        reader.readAsText(file);

    }

    // Excel file
    else {

        alert("Excel file selected.\nTarget column detection will be available after backend upload.");

    }

});

// ==========================
// Analyze Button
// ==========================

analyzeBtn.addEventListener("click", function () {

    const file = fileInput.files[0];

    if (!file) {

        alert("Please upload a dataset.");
        return;

    }

    if (!algorithm.value) {

        alert("Please select an algorithm.");
        return;

    }

    if (!targetColumn.value) {

        alert("Please select a target column.");
        return;

    }

    const formData = new FormData();

formData.append("file", file);
formData.append("algorithm", algorithm.value);
formData.append("target_column", targetColumn.value);

fetch("/upload", {
    method: "POST",
    body: formData
})

.then(response => response.json())

.then(data => {

    loading.classList.add("hidden");

    console.log(data);

    if (!data.success) {

        alert(data.message);
        return;

    }

    results.innerHTML = `

        <div class="result-card">

            <h2>Analysis Complete ✅</h2>

            <br>

            <h3>Dataset Information</h3>

            <p><b>Rows:</b> ${data.dataset_info.rows}</p>

            <p><b>Columns:</b> ${data.dataset_info.columns}</p>

            <br>

            <h3>Health Report</h3>

            <p><b>Status:</b> ${data.health_report.status}</p>

            <p><b>Score:</b> ${data.health_report.health_score}/100</p>

            <br>

            <h3>Insights</h3>

            <ul>

                ${data.insights.map(i => `<li>${i}</li>`).join("")}

            </ul>

            <br>

            <h3>AI Executive Summary</h3>

            <p>${data.ai_insights.executive_summary}</p>

        </div>

    `;

})

.catch(error => {

    loading.classList.add("hidden");

    console.error(error);

    alert("Error connecting to backend.");

})})