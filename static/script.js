const fileInput =
    document.getElementById("logFile");

const fileName =
    document.getElementById("fileName");

const loader =
    document.getElementById("loader");

fileInput.addEventListener(
    "change",
    () => {

        if (
            fileInput.files.length > 0
        ) {
            fileName.textContent =
                fileInput.files[0].name;
        }
    }
);

async function analyzeLogs() {

    const resultsDiv =
        document.getElementById(
            "results"
        );

    if (
        !fileInput.files[0]
    ) {
        alert(
            "Please upload a log file"
        );
        return;
    }

    const formData =
        new FormData();

    formData.append(
        "logfile",
        fileInput.files[0]
    );

    loader.style.display =
        "block";

    resultsDiv.innerHTML = "";

    try {

        const response =
            await fetch(
                "/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );

        const data =
            await response.json();

        loader.style.display =
            "none";

        let html = "";

        if (
            data.length === 0
        ) {
            html = `
            <div class="result-card">
                No incidents found.
            </div>`;
        }

        data.forEach(
            (item, index) => {

            const severity =
                item.severity
                    .toLowerCase();

            html += `
            <div class="result-card">

                <div class="result-header">

                    <h2>
                        Incident ${index + 1}
                    </h2>

                    <span class="badge ${severity}">
                        ${item.severity}
                    </span>

                </div>

                <p>
                    <b>Category:</b>
                    ${item.category}
                </p>

                <p>
                    <b>Root Cause:</b>
                    ${item.root_cause}
                </p>

                <p>
                    <b>Suggested Fix:</b>
                    ${item.suggested_fix}
                </p>

            </div>
            `;
        });

        resultsDiv.innerHTML =
            html;

    } catch (error) {

        loader.style.display =
            "none";

        resultsDiv.innerHTML =
            `
        <div class="result-card">
            Error analyzing logs.
            Please try again.
        </div>
        `;

        console.error(error);
    }
}