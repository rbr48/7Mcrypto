/**
 * 4D Crypto Risk Interactive Web Quant Lab Simulation
 * Author: Izhaan Intellect Research Group (https://7mcrypto.izhaanintellect.fun/)
 */

// 7 Major Cryptocurrency Assets
const ASSETS = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE"];

// Empirical 7x7 GIRF Volatility Spillover Matrix (%)
const BASE_SPILLOVER = [
  [38.4, 21.2, 14.8,  8.2,  6.4,  5.8,  5.2], // BTC
  [19.8, 36.2, 18.4,  9.5,  6.1,  5.2,  4.8], // ETH
  [16.2, 17.5, 41.0,  8.1,  6.8,  5.4,  5.0], // SOL
  [ 9.4,  8.8,  7.6, 52.3,  8.1,  7.2,  6.6], // BNB
  [ 7.1,  6.5,  6.8,  8.4, 55.2,  8.6,  7.4], // XRP
  [ 6.5,  5.8,  6.2,  7.5,  9.1, 56.4,  8.5], // ADA
  [ 5.8,  5.1,  5.5,  6.9,  8.2,  9.0, 59.5]  // DOGE
];

// Pre-computed Sensitivity Lookup Table from Table 3 in the Research Paper
const SENSITIVITY_TABLE = {
  // Key: `${threshold}_${hysteresis}`
  "0.10_false": { sharpe: 1.84, dd: -19.5, flips: 64, friction: 0, returnMult: 3.42 },
  "0.10_true":  { sharpe: 1.98, dd: -15.8, flips: 26, friction: 240, returnMult: 3.75 },
  "0.15_false": { sharpe: 1.86, dd: -19.1, flips: 58, friction: 20, returnMult: 3.55 },
  "0.15_true":  { sharpe: 2.02, dd: -14.9, flips: 22, friction: 285, returnMult: 3.90 },
  "0.20_false": { sharpe: 1.88, dd: -18.4, flips: 56, friction: 40, returnMult: 3.65 },
  "0.20_true":  { sharpe: 2.06, dd: -14.1, flips: 20, friction: 320, returnMult: 4.02 },
  "0.25_false": { sharpe: 1.95, dd: -16.2, flips: 48, friction: 95, returnMult: 3.78 },
  "0.25_true":  { sharpe: 2.10, dd: -13.5, flips: 19, friction: 355, returnMult: 4.14 },
  "0.30_false": { sharpe: 1.92, dd: -15.1, flips: 41, friction: 140, returnMult: 3.82 },
  "0.30_true":  { sharpe: 2.14, dd: -12.9, flips: 18, friction: 379, returnMult: 4.207 }, // Optimal
  "0.35_false": { sharpe: 1.81, dd: -17.8, flips: 32, friction: 180, returnMult: 3.52 },
  "0.35_true":  { sharpe: 2.08, dd: -14.2, flips: 16, friction: 392, returnMult: 3.98 },
  "0.40_false": { sharpe: 1.68, dd: -22.4, flips: 24, friction: 220, returnMult: 3.12 },
  "0.40_true":  { sharpe: 1.98, dd: -15.8, flips: 12, friction: 420, returnMult: 3.68 },
};

// UI State
let currentThreshold = 0.30;
let hysteresisActive = true;
let equityChart = null;

// Initialize Matrix Heatmap
function renderSpilloverMatrix() {
  const container = document.getElementById("matrixContainer");
  container.innerHTML = "";

  // Corner blank
  const corner = document.createElement("div");
  corner.className = "matrix-cell header";
  corner.textContent = "To \\ From";
  container.appendChild(corner);

  // Column Headers
  ASSETS.forEach(asset => {
    const colHeader = document.createElement("div");
    colHeader.className = "matrix-cell header";
    colHeader.textContent = asset;
    container.appendChild(colHeader);
  });

  // Rows
  for (let i = 0; i < ASSETS.length; i++) {
    // Row Header
    const rowHeader = document.createElement("div");
    rowHeader.className = "matrix-cell header";
    rowHeader.textContent = ASSETS[i];
    container.appendChild(rowHeader);

    // Cells
    for (let j = 0; j < ASSETS.length; j++) {
      const cell = document.createElement("div");
      cell.className = "matrix-cell";
      const val = BASE_SPILLOVER[i][j];
      cell.textContent = val.toFixed(1) + "%";

      if (i === j) {
        cell.classList.add("diagonal");
      } else {
        // Color intensity based on spillover %
        if (val > 15.0) {
          cell.style.background = "#fee2e2";
          cell.style.color = "#991b1b";
          cell.style.borderColor = "#fca5a5";
        } else if (val > 8.0) {
          cell.style.background = "#fef3c7";
          cell.style.color = "#92400e";
          cell.style.borderColor = "#fde68a";
        } else {
          cell.style.background = "#ecfdf5";
          cell.style.color = "#065f46";
        }
      }
      cell.title = `Spillover from ${ASSETS[j]} to ${ASSETS[i]}: ${val.toFixed(1)}%`;
      container.appendChild(cell);
    }
  }
}

// Generate Synthetic Walk-Forward Equity Curves
function generateEquityData(returnMult, maxDD) {
  const points = 48; // 24 months (semi-monthly)
  const labels = [];
  const spotEquity = [];
  const hedgedEquity = [];

  let s = 100.0;
  let h = 100.0;

  for (let i = 0; i < points; i++) {
    const month = Math.floor(i / 2) + 1;
    const isMid = i % 2 === 1;
    labels.push(`M${month}${isMid ? '.5' : ''}`);

    // Market simulation: Bull trend with August 2024 shock at step 38
    if (i === 38) {
      // The August 5 Yen Shock
      s = s * (1.0 - 0.38); // -38% instant spot crash
      h = h * (1.0 - (Math.abs(maxDD) / 100.0 * 0.4)); // Hedged cushions the shock
    } else if (i > 38 && i <= 42) {
      // Rebound phase
      s = s * 1.05;
      h = h * 1.03;
    } else {
      // Baseline drift
      s = s * (1.0 + (Math.sin(i * 0.4) * 0.04 + 0.015));
      const hedgeGrowth = Math.pow(returnMult, 1 / points);
      h = h * (hedgeGrowth + (Math.cos(i * 0.3) * 0.01));
    }

    spotEquity.push(parseFloat(s.toFixed(1)));
    hedgedEquity.push(parseFloat(h.toFixed(1)));
  }

  return { labels, spotEquity, hedgedEquity };
}

// Initialize / Update Chart.js
function updateChart(returnMult, maxDD) {
  const { labels, spotEquity, hedgedEquity } = generateEquityData(returnMult, maxDD);

  if (!equityChart) {
    const ctx = document.getElementById("equityChart").getContext("2d");
    equityChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "M5 LightGBM + Hysteresis (Hedged)",
            data: hedgedEquity,
            borderColor: "#10b981",
            backgroundColor: "rgba(16, 185, 129, 0.08)",
            borderWidth: 2.5,
            fill: true,
            tension: 0.25,
            pointRadius: 0,
            pointHoverRadius: 5
          },
          {
            label: "M0 Benchmark (Unhedged Spot)",
            data: spotEquity,
            borderColor: "#e11d48",
            borderWidth: 1.8,
            borderDash: [5, 4],
            fill: false,
            tension: 0.25,
            pointRadius: 0,
            pointHoverRadius: 5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: {
            position: "top",
            labels: { font: { family: "monospace", size: 11 }, boxWidth: 14 }
          },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: $${ctx.parsed.y}`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { font: { family: "monospace", size: 10 }, maxTicksLimit: 12 }
          },
          y: {
            grid: { color: "#f1f5f9" },
            ticks: { font: { family: "monospace", size: 10 }, callback: (v) => `$${v}` }
          }
        }
      }
    });
  } else {
    equityChart.data.datasets[0].data = hedgedEquity;
    equityChart.data.datasets[1].data = spotEquity;
    equityChart.update();
  }
}

// Update Dashboard State
function updateSimulation() {
  const key = `${currentThreshold.toFixed(2)}_${hysteresisActive}`;
  const data = SENSITIVITY_TABLE[key] || SENSITIVITY_TABLE["0.30_true"];

  // Update UI Elements
  document.getElementById("thresholdVal").textContent = currentThreshold.toFixed(2);
  document.getElementById("kpiSharpe").textContent = data.sharpe.toFixed(2);
  document.getElementById("kpiDrawdown").textContent = `${data.dd.toFixed(1)}%`;
  document.getElementById("kpiFlips").textContent = data.flips;
  document.getElementById("kpiFriction").textContent = `+${data.friction} bps`;

  updateChart(data.returnMult, data.dd);
}

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  renderSpilloverMatrix();
  updateSimulation();

  const slider = document.getElementById("thresholdSlider");
  slider.addEventListener("input", (e) => {
    currentThreshold = parseFloat(e.target.value);
    updateSimulation();
  });

  const hBtn = document.getElementById("hysteresisBtn");
  hBtn.addEventListener("click", () => {
    hysteresisActive = !hysteresisActive;
    if (hysteresisActive) {
      hBtn.className = "btn-toggle active";
      hBtn.textContent = "ENABLED (Δ = 0.15 Deadband)";
    } else {
      hBtn.className = "btn-toggle";
      hBtn.textContent = "DISABLED (Point-in-Time Whipsaw)";
    }
    updateSimulation();
  });
});
