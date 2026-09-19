const assetsContainer = document.getElementById("assetsContainer");
const addAssetButton = document.getElementById("addAsset");
const analyzeButton = document.getElementById("analyzeButton");

const totalWeightDisplay = document.getElementById("totalWeight");
const errorMessage = document.getElementById("errorMessage");

// -----------------
//add assets
//------------------
addAssetButton.addEventListener("click", function () {
    const row = document.createElement("div");
    row.className = "asset-row";
    row.innerHTML = `
        <div>
            <label>Ticker</label>

            <input
                type="text"
                class="ticker"
                placeholder="GOOGL"
            >
        </div>
        <div>
            <label>Weight</label>

            <div class="percentage-input">
                <input
                    type="number"
                    class="weight"
                    placeholder="20"
                    min="0"
                    max="100"
                >

                <span>%</span>
            </div>
        </div>
        <button class="remove-button">
            ×
        </button>
    `;
    assetsContainer.appendChild(row);
    updateTotal();
});

// ------------------
// remove asset
// ------------------
assetsContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-button")) {
        event.target.parentElement.remove();
        updateTotal();
    }
});

// ---------------------
//update toala
// ---------------------
assetsContainer.addEventListener("input", function () {
    updateTotal();
});

function updateTotal() {
    const weights = document.querySelectorAll(".weight");
    let total = 0;
    weights.forEach(function (input) {
        const value = Number(input.value) || 0;
        total += value;
    });
    totalWeightDisplay.textContent = total.toFixed(1) + "%";
    if (total === 100) {
        totalWeightDisplay.style.color = "#1e9c5b";
    } else {
        totalWeightDisplay.style.color = "#64C7FF";
    }
}

//------------------
// analyze portfoilio
//------------------
analyzeButton.addEventListener("click", function () {
    errorMessage.textContent = "";
    const portfolioValue = 
        Number(document.getElementById("portfolioValue").value);
    const tickerInputs = 
        document.querySelectorAll(".ticker");
    const weightInputs = 
        document.querySelectorAll(".weight");
    //checking portfolio $$
    if (!portfolioValue || portfolioValue <= 0) {
        errorMessage.textContent = 
            "please enter valid portfolio value.";
        return;
    }
    let totalWeight = 0;
    const assets = [];
    for (let i = 0; i < tickerInputs.length; i++) {
        const ticker = 
            tickerInputs[i].value.trim().toUpperCase();
        const weight = 
            Number(weightInputs[i].value) || 0;
        if(!ticker){
            errorMessage.textContent = 
                "please enter a ticker for every asset.";
            return;
        }
        if (weight <= 0) {
            errorMessage.textContent = 
                "every asset must have a weight greater than 0.";
            return;
        }

        totalWeight += weight;
        assets.push({
            ticker:ticker,
            weight:weight
        });
    }
    //fake demo results for nwo
    generateDemoResults(portfolioValue, assets);
});

//----------------------
//demo results
//----------------------
function generateDemoResults(portfolioValue, assets) {
    //numebrs temp later will calculate results
    document.getElementById("returnResult").textContent = 
        "11.7%";
    document.getElementById("volatilityResult").textContent =
        "19.4%";
    document.getElementById("sharpeResult").textContent =
        "0.52";
    document.getElementById("varResult").textContent =
        "$218";
    //alocation
    const allocation = 
        document.getElementById("allocationResults");
    allocation.innerHTML = "";
    assets.forEach(function (asset) {
        const amount = 
            portfolioValue * (asset.weight / 100);
        const item = document.createElement("div");
        item.style.display = "flex";
        item.style.justifyContent = "space-between";
        item.style.padding = "12px 0";
        item.style.borderBottom = "1px solid #1B496E";

        item.innerHTML = `
            <span>
                ${asset.ticker}
            </span>
            <span style="color: #64C7FF">
                ${asset.weight}%
                ($${amount.toLocaleString()})
            </span>
        `;
        allocation.appendChild(item);
    });
    //results show
    const results = 
        document.getElementById("results");
    results.classList.remove("hidden");
    results.scrollIntoView({
        behavior: "smooth"
    });
}
//intial calcualtiosn
updateTotal();