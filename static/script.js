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

    fileName.textContent = file.name;

    targetColumn.innerHTML =
        '<option value="">Select Target</option>';

    if (file.name.toLowerCase().endsWith(".csv")) {

        const reader = new FileReader();

        reader.onload = function (e) {

            const csv = e.target.result;

            const firstLine = csv.split(/\r?\n/)[0];

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

    else {

        alert("Excel detected. Target columns will be loaded after upload.");

    }

});

// ==========================
// Analyze Dataset
// ==========================

analyzeBtn.addEventListener("click", async function () {

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

    loading.classList.remove("hidden");
    results.innerHTML = "";

    const formData = new FormData();

    formData.append("file", file);
    formData.append("algorithm", algorithm.value);
    formData.append("target_column", targetColumn.value);

    try {

        const response = await fetch("/upload", {

            method: "POST",
            body: formData

        });

        console.log("Status:", response.status);

        const text = await response.text();

        console.log(text);

        const data = JSON.parse(text);

        loading.classList.add("hidden");

        if (!data.success) {

            alert(data.message);
            return;

        }

        const summary =
            data.ai_insights?.executive_summary ??
            "No AI Executive Summary Available.";

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

                    ${data.insights.map(item => `<li>${item}</li>`).join("")}

                </ul>

                <br>

                <h3>AI Executive Summary</h3>

                <p>${summary}</p>

            </div>

        `;

    }

    catch (error) {

        loading.classList.add("hidden");

        console.error(error);

        alert(error.message);

    }

});