// ==========================
// Get HTML Elements
// ==========================

const fileInput = document.getElementById("datasetFile");
const targetColumn = document.getElementById("targetColumn");
const analyzeBtn = document.getElementById("analyzeBtn");



fileInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    console.log("Selected File:", file.name);

    
    const uploadText = document.querySelector(".upload-box p");

    uploadText.textContent = file.name;

   
    if (!file.name.endsWith(".csv")) {

        targetColumn.innerHTML =
            "<option>Select Target</option>";

        alert("Target column detection currently supports CSV files only.");

        return;
    }

    const reader = new FileReader();

    reader.onload = function (event) {

        const csv = event.target.result;

        
        const firstLine = csv.split("\n")[0];

        // Split into column names
        const columns = firstLine.split(",");

        // Clear previous options
        targetColumn.innerHTML = "";

        // Add default option
        const defaultOption = document.createElement("option");

        defaultOption.textContent = "Select Target";

        defaultOption.value = "";

        targetColumn.appendChild(defaultOption);

        // Add all columns
        columns.forEach(column => {

            const option = document.createElement("option");

            option.value = column.trim();

            option.textContent = column.trim();

            targetColumn.appendChild(option);

        });

        console.log("Columns:", columns);

    };

    reader.readAsText(file);

});

// ==========================
// Analyze Button
// ==========================

analyzeBtn.addEventListener("click", function () {

    const file = fileInput.files[0];

    const target = targetColumn.value;

    const algorithm =
        document.getElementById("algorithm").value;

    if (!file) {

        alert("Please upload a dataset.");

        return;

    }

    if (!algorithm) {

        alert("Please select an algorithm.");

        return;

    }

    if (!target) {

        alert("Please select a target column.");

        return;

    }

    console.log("Ready to Analyze");

    console.log("File:", file.name);

    console.log("Algorithm:", algorithm);

    console.log("Target:", target);

    // Flask API connection comes next.

});// ============================
// Elements
// ============================

const fileInput = document.getElementById("datasetFile");
const targetColumn = document.getElementById("targetColumn");
const fileName = document.getElementById("fileName");

// ============================
// File Upload
// ============================

fileInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    // Show filename

    fileName.textContent = file.name;

    // Only CSV header detection for now

    if (!file.name.toLowerCase().endsWith(".csv")) {

        targetColumn.innerHTML =
            '<option value="">Select Target</option>';

        return;

    }

    const reader = new FileReader();

    reader.onload = function (event) {

        const csv = event.target.result;

        const firstLine = csv.split(/\r?\n/)[0];

        // Detect delimiter

        const delimiter = firstLine.includes(";") ? ";" : ",";

        const headers = firstLine.split(delimiter);

        targetColumn.innerHTML =
            '<option value="">Select Target</option>';

        headers.forEach(header => {

            const option = document.createElement("option");

            option.value = header.trim();

            option.textContent = header.trim();

            targetColumn.appendChild(option);

        });

    };

    reader.readAsText(file);

});