
const fileInput = document.getElementById("datasetFile");
const fileName = document.getElementById("fileName");
const targetColumn = document.getElementById("targetColumn");
const algorithm = document.getElementById("algorithm");
const analyzeBtn = document.getElementById("analyzeBtn");
const loading = document.getElementById("loading");
const results = document.getElementById("results");


const datasetCard = document.getElementById("datasetCard");
const healthCard = document.getElementById("healthCard");
const preprocessingCard = document.getElementById("preprocessingCard");
const mlCard = document.getElementById("mlCard");
const aiCard = document.getElementById("aiCard");
const chartsCard = document.getElementById("chartsCard");



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

            const delimiter =
                firstLine.includes(";")
                    ? ";"
                    : ",";

            const headers =
                firstLine.split(delimiter);

            headers.forEach(header => {

                const option =
                    document.createElement("option");

                option.value = header.trim();

                option.textContent = header.trim();

                targetColumn.appendChild(option);

            });

        };

        reader.readAsText(file);

    }

    else {

        alert(
            "Excel detected. Target columns will be available after upload."
        );

    }

});



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

    results.classList.add("hidden");

    const formData = new FormData();

    formData.append("file", file);

    formData.append("algorithm", algorithm.value);

    formData.append("target_column", targetColumn.value);

    try {

        const response = await fetch("/upload", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        loading.classList.add("hidden");

        if (!data.success) {

            alert(data.message);

            return;

        }

        results.classList.remove("hidden");

       

        datasetCard.innerHTML = `

            <h2>📄 Dataset Information</h2>

            <p><b>Dataset:</b> ${data.filename}</p>

            <p><b>Rows:</b> ${data.dataset_info.rows}</p>

            <p><b>Columns:</b> ${data.dataset_info.columns}</p>

            <p><b>Column Names:</b></p>

            <ul>

                ${data.dataset_info.column_names
                    .map(column => `<li>${column}</li>`)
                    .join("")}

            </ul>

        `;



        healthCard.innerHTML = `

            <h2>❤️ Dataset Health</h2>

            <p><b>Status:</b> ${data.health_report.status}</p>

            <p><b>Health Score:</b> ${data.health_report.health_score}/100</p>

            <p><b>Missing Values:</b> ${data.health_report.total_missing_values}</p>

            <p><b>Duplicate Rows:</b> ${data.health_report.duplicate_rows}</p>

        `;



        preprocessingCard.innerHTML = `

            <h2>🧹 Preprocessing Report</h2>

            <p><b>Missing Strategy:</b>

                ${data.preprocessing?.missing_values?.strategy ?? "N/A"}

            </p>

            <p><b>Remaining Missing Values:</b>

                ${data.preprocessing?.missing_values?.remaining_missing_values ?? 0}

            </p>

            <p><b>Encoding:</b>

                ${data.preprocessing?.encoding?.method ??
                  data.preprocessing?.encoding ??
                  "N/A"}

            </p>

            <p><b>Scaling:</b>

                ${data.preprocessing?.scaling?.method ??
                  data.preprocessing?.scaling ??
                  "N/A"}

            </p>

            <p>

                <b>Final Shape:</b>

                ${data.preprocessing.final_shape.rows}

                ×

                ${data.preprocessing.final_shape.columns}

            </p>

        `;
            

        const ml = data.machine_learning;

        if (ml) {

            let metricsHTML = "";

            if (ml.metrics) {

                metricsHTML = Object.entries(ml.metrics)

                    .map(

                        ([key, value]) =>

                        `<p><b>${key}:</b> ${value}</p>`

                    )

                    .join("");

            }

            let featureHTML = "";

            if (

                ml.feature_importance &&

                Object.keys(ml.feature_importance).length > 0

            ) {

                featureHTML = `

                    <h3>Feature Importance</h3>

                    <ul>

                        ${Object.entries(ml.feature_importance)

                            .map(

                                ([feature, score]) =>

                                `<li><b>${feature}</b> : ${score}</li>`

                            )

                            .join("")}

                    </ul>

                `;

            }

            mlCard.innerHTML = `

                <h2>📈 Machine Learning</h2>

                <p>

                    <b>Algorithm:</b>

                    ${ml.algorithm}

                </p>

                ${metricsHTML}

                ${featureHTML}

            `;

        }

        else {

            mlCard.innerHTML = `

                <h2>📈 Machine Learning</h2>

                <p>No Machine Learning model was executed.</p>

            `;

        }


        const ai = data.ai_insights;

        aiCard.innerHTML = `

            <h2>🤖 AI Insights</h2>

            <h3>Executive Summary</h3>

            <p>

                ${ai?.executive_summary ?? "No Executive Summary"}

            </p>

            <h3>Key Insights</h3>

            <ul>

                ${data.insights

                    .map(

                        insight =>

                        `<li>${insight}</li>`

                    )

                    .join("")}

            </ul>

        `;
          

        const charts = data.visualizations;

        if (charts && Object.keys(charts).length > 0) {

            let chartHTML = `<h2>📊 Visualizations</h2>`;

            Object.entries(charts).forEach(([title, image]) => {

                chartHTML += `

                    <div class="chart-card">

                        <h3>${title.replaceAll("_", " ")}</h3>

                        <img src="${image}" alt="${title}">

                    </div>

                `;

            });

            chartsCard.innerHTML = chartHTML;

        }

        else {

            chartsCard.innerHTML = `

                <h2>📊 Visualizations</h2>

                <p>No visualizations generated.</p>

            `;

        }

    }

    catch (error) {

        loading.classList.add("hidden");

        console.error(error);

        alert("Error: " + error.message);

    }

});