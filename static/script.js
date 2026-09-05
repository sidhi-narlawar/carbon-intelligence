async function loadDashboard() {

    const response = await fetch("/api/dashboard");
    const data = await response.json();

    document.getElementById("total").innerText = data.total;
    document.getElementById("scope1").innerText = data.scope1;
    document.getElementById("scope2").innerText = data.scope2;
    document.getElementById("scope3").innerText = data.scope3;
}


async function addActivity() {

    const activity = document.getElementById("activity").value;
    const amount = Number(document.getElementById("amount").value);
    const date = document.getElementById("date").value;

    if (!amount || !date) {
        alert("Please enter amount and date");
        return;
    }

    await fetch("/api/activities", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            activity_type: activity,
            amount: amount,
            date: date
        })
    });

    document.getElementById("amount").value = "";

    loadDashboard();
    loadActivities();
    loadAnomalies();

    alert("Activity added successfully!");
}


async function loadActivities() {

    const response = await fetch("/api/activities");
    const data = await response.json();

    const table = document.getElementById("activities");

    table.innerHTML = "";

    data.forEach(a => {

        table.innerHTML += `
            <tr>
                <td>${a.activity}</td>
                <td>${a.amount} ${a.unit}</td>
                <td>Scope ${a.scope}</td>
                <td>${a.emissions.toFixed(2)} kg CO₂e</td>
            </tr>
        `;

    });
}


async function calculateScenario() {

    const reduction =
        Number(document.getElementById("reduction").value);

    if (!reduction) {
        alert("Enter reduction percentage");
        return;
    }

    const response =
        await fetch(`/api/scenario?reduction=${reduction}`);

    const data = await response.json();

    document.getElementById("scenario").innerHTML = `
        <h3>Scenario Result</h3>

        <p>Current emissions:
        <b>${data.current_emissions} kg CO₂e</b></p>

        <p>Reduction:
        <b>${data.reduction_percent}%</b></p>

        <p>Potential reduction:
        <b>${data.reduction_amount} kg CO₂e</b></p>

        <p>Projected emissions:
        <b>${data.projected_emissions} kg CO₂e</b></p>
    `;
}


async function loadAnomalies() {

    const response = await fetch("/api/anomalies");
    const data = await response.json();

    const element = document.getElementById("anomalies");

    if (data.length === 0) {

        element.innerHTML =
            "✅ No unusual activity detected.";

        return;
    }

    element.innerHTML = data.map(a => `
        <p>
            ⚠️ <b>${a.activity}</b>:
            ${a.message}
            (${a.amount})
        </p>
    `).join("");
}


loadDashboard();
loadActivities();
loadAnomalies();
async function loadCharts() {

    const response = await fetch("/api/activities");
    const data = await response.json();

    const scopeTotals = {
        "Scope 1": 0,
        "Scope 2": 0,
        "Scope 3": 0
    };

    const activityTotals = {};

    data.forEach(a => {

        scopeTotals[`Scope ${a.scope}`] += a.emissions;

        if (!activityTotals[a.activity]) {
            activityTotals[a.activity] = 0;
        }

        activityTotals[a.activity] += a.emissions;
    });


    new Chart(document.getElementById("scopeChart"), {

        type: "doughnut",

        data: {
            labels: Object.keys(scopeTotals),

            datasets: [{
                data: Object.values(scopeTotals)
            }]
        }
    });


    new Chart(document.getElementById("activityChart"), {

        type: "bar",

        data: {
            labels: Object.keys(activityTotals),

            datasets: [{
                label: "kg CO₂e",
                data: Object.values(activityTotals)
            }]
        },

        options: {
            responsive: true
        }
    });
}

loadCharts();
async function loadSuppliers() {
    const response = await fetch("/api/suppliers");
    const suppliers = await response.json();

    document.getElementById("supplierTable").innerHTML =
        suppliers.map(s => `
            <tr>
                <td>${s.name}</td>
                <td>${s.category}</td>
                <td>${s.emissions} kg CO₂e</td>
                <td>${s.carbon_score}/100</td>
            </tr>
        `).join("");
}

loadSuppliers();
async function addSupplier() {

    const name = document.getElementById("supplierName").value;
    const category = document.getElementById("supplierCategory").value;
    const emissions = Number(document.getElementById("supplierEmissions").value);
    const carbon_score = Number(document.getElementById("supplierScore").value);

    if (!name || !category || !emissions || !carbon_score) {
        alert("Please fill all supplier fields");
        return;
    }

    await fetch("/api/suppliers", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            category,
            emissions,
            carbon_score
        })
    });

    document.getElementById("supplierName").value = "";
    document.getElementById("supplierCategory").value = "";
    document.getElementById("supplierEmissions").value = "";
    document.getElementById("supplierScore").value = "";

    loadSuppliers();
}