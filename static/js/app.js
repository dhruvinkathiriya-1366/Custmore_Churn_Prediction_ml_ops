document.addEventListener("DOMContentLoaded", () => {

  // =========================================================
  // 0. Pure Diamond / Hexagon Grid Lightning & Glow Engine
  // =========================================================
  const canvas = document.getElementById("lightning-canvas");
  
  let mouseX = -9999;
  let mouseY = -9999;
  let isMouseOnScreen = false;

  window.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    isMouseOnScreen = true;
  });

  window.addEventListener("mouseenter", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    isMouseOnScreen = true;
  });

  window.addEventListener("mouseleave", () => {
    isMouseOnScreen = false;
    mouseX = -9999;
    mouseY = -9999;
  });

  // Hexagon Honeycomb Canvas Renderer
  if (canvas) {
    const ctx = canvas.getContext("2d");
    let width = 0;
    let height = 0;
    let dpr = window.devicePixelRatio || 1;

    const hexRadius = 32; // Hexagon radius
    const hexWidth = Math.sqrt(3) * hexRadius; // ~55.42px
    const hexVertSpacing = 1.5 * hexRadius;   // 48px
    const hoverRadius = 160; // Focused mouse illumination radius

    let hexagons = [];
    const ripples = [];

    // Precalculate vertices for a pointy-topped hexagon centered at (0,0)
    const baseVertices = [];
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 6) + (i * Math.PI) / 3;
      baseVertices.push({
        x: hexRadius * Math.cos(angle),
        y: hexRadius * Math.sin(angle)
      });
    }

    function initHexGrid() {
      dpr = window.devicePixelRatio || 1;
      width = window.innerWidth;
      height = window.innerHeight;

      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.scale(dpr, dpr);

      hexagons = [];

      const cols = Math.ceil(width / hexWidth) + 3;
      const rows = Math.ceil(height / hexVertSpacing) + 3;

      for (let r = -1; r < rows; r++) {
        const rowOffsetY = r * hexVertSpacing;
        const colOffsetX = (r % 2 === 0 ? 0 : hexWidth / 2) - hexWidth;

        for (let c = -1; c < cols; c++) {
          const cx = colOffsetX + c * hexWidth;
          const cy = rowOffsetY;

          hexagons.push({
            cx,
            cy,
            energy: 0
          });
        }
      }
    }

    window.addEventListener("resize", () => {
      initHexGrid();
    });
    initHexGrid();

    // Helper: draw single hexagon path
    function buildHexPath(cx, cy, scale = 1.0) {
      ctx.beginPath();
      for (let i = 0; i < 6; i++) {
        const vx = cx + baseVertices[i].x * scale;
        const vy = cy + baseVertices[i].y * scale;
        if (i === 0) ctx.moveTo(vx, vy);
        else ctx.lineTo(vx, vy);
      }
      ctx.closePath();
    }

    const sparks = [];

    // Helper: draw electric lightning surge along an exact grid edge segment
    function drawEdgeLightning(x1, y1, x2, y2, intensity = 1.0, color = "#00f0ff") {
      const dx = x2 - x1;
      const dy = y2 - y1;
      const len = Math.hypot(dx, dy);
      const steps = 5;

      ctx.beginPath();
      ctx.moveTo(x1, y1);

      for (let s = 1; s < steps; s++) {
        const t = s / steps;
        // Jitter perpendicular to the edge
        const perpX = -dy / len;
        const perpY = dx / len;
        const jitter = (Math.random() - 0.5) * 4.5 * intensity;

        const px = x1 + dx * t + perpX * jitter;
        const py = y1 + dy * t + perpY * jitter;
        ctx.lineTo(px, py);
      }

      ctx.lineTo(x2, y2);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2 + intensity * 1.5;
      ctx.shadowColor = "#00f0ff";
      ctx.shadowBlur = 14 * intensity;
      ctx.stroke();

      // White lightning core for high intensity
      if (intensity > 0.55) {
        ctx.strokeStyle = `rgba(255, 255, 255, ${(intensity - 0.55) * 2.5})`;
        ctx.lineWidth = 1.0;
        ctx.shadowColor = "#ffffff";
        ctx.shadowBlur = 10;
        ctx.stroke();
      }
    }

    let lastFrameTime = performance.now();

    function renderHexagonEngine(timestamp) {
      const dt = (timestamp - lastFrameTime) / 1000;
      lastFrameTime = timestamp;

      ctx.clearRect(0, 0, width, height);

      const activeHexagons = [];

      // Update Hexagon energies based ONLY on active mouse hover
      for (let i = 0; i < hexagons.length; i++) {
        const hex = hexagons[i];

        // 1. Mouse distance illumination only when mouse is active on screen
        if (isMouseOnScreen) {
          const dx = hex.cx - mouseX;
          const dy = hex.cy - mouseY;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < hoverRadius) {
            const factor = Math.pow(1 - dist / hoverRadius, 1.8);
            hex.energy = Math.max(hex.energy, factor);
          }
        }

        // 2. Responsive smooth exponential decay
        hex.energy *= 0.86;
        if (hex.energy < 0.005) hex.energy = 0;

        if (hex.energy > 0.01) {
          activeHexagons.push(hex);
        }
      }

      // -----------------------------------------------------
      // Pass 1: Render All Base Hexagon Outlines (Crisp, Elegant Dark Diamond Grid)
      // -----------------------------------------------------
      ctx.lineWidth = 1.1;
      ctx.shadowBlur = 0;
      ctx.strokeStyle = "rgba(0, 170, 255, 0.14)"; // Elegant, visible dark cyan-blue lattice

      ctx.beginPath();
      for (let i = 0; i < hexagons.length; i++) {
        const hex = hexagons[i];
        for (let v = 0; v < 6; v++) {
          const vx = hex.cx + baseVertices[v].x;
          const vy = hex.cy + baseVertices[v].y;
          if (v === 0) ctx.moveTo(vx, vy);
          else ctx.lineTo(vx, vy);
        }
        ctx.closePath();
      }
      ctx.stroke();

      // Subtle vertex points on dark grid for high-tech aesthetic
      ctx.fillStyle = "rgba(0, 220, 255, 0.22)";
      for (let i = 0; i < hexagons.length; i += 2) {
        const hex = hexagons[i];
        for (let v = 0; v < 6; v++) {
          const vx = hex.cx + baseVertices[v].x;
          const vy = hex.cy + baseVertices[v].y;
          ctx.fillRect(vx - 0.75, vy - 0.75, 1.5, 1.5);
        }
      }

      // -----------------------------------------------------
      // Pass 2: Render Glowing Diamond / Hexagon Borders (NO Inside Fill)
      // -----------------------------------------------------
      for (let i = 0; i < activeHexagons.length; i++) {
        const hex = activeHexagons[i];
        const energy = hex.energy;

        buildHexPath(hex.cx, hex.cy, 1.0);

        // Neon Blue Hexagon Border along grid
        ctx.strokeStyle = `rgba(0, 240, 255, ${Math.min(0.3 + energy * 0.7, 1)})`;
        ctx.lineWidth = 1.3 + energy * 2.2;
        ctx.shadowColor = "#00f0ff";
        ctx.shadowBlur = energy * 22;
        ctx.stroke();

        // White-Hot Electric Core along the Border for Closest Cells
        if (energy > 0.45) {
          const coreAlpha = (energy - 0.45) * 1.85;
          ctx.strokeStyle = `rgba(255, 255, 255, ${Math.min(coreAlpha, 1.0)})`;
          ctx.lineWidth = 1.6;
          ctx.shadowColor = "#ffffff";
          ctx.shadowBlur = 12;
          ctx.stroke();
        }
      }

      // -----------------------------------------------------
      // Pass 3: Electric Lightning Surges & High-Voltage Sparks Along Diamond Borders
      // -----------------------------------------------------
      if (activeHexagons.length > 0) {
        for (let i = 0; i < activeHexagons.length; i++) {
          const hex = activeHexagons[i];
          if (hex.energy > 0.25) {
            // Draw electric lightning micro-surges along active hexagon edges
            for (let e = 0; e < 6; e++) {
              const v1 = baseVertices[e];
              const v2 = baseVertices[(e + 1) % 6];
              const x1 = hex.cx + v1.x;
              const y1 = hex.cy + v1.y;
              const x2 = hex.cx + v2.x;
              const y2 = hex.cy + v2.y;

              if (Math.random() < hex.energy * 0.75) {
                drawEdgeLightning(
                  x1,
                  y1,
                  x2,
                  y2,
                  hex.energy,
                  `rgba(0, 240, 255, ${Math.min(hex.energy * 1.3, 1)})`
                );

                // Spawn vivid electric sparks flying off the lightning wire
                if (Math.random() < hex.energy * 0.55 && sparks.length < 140) {
                  const t = Math.random();
                  const sx = x1 * (1 - t) + x2 * t;
                  const sy = y1 * (1 - t) + y2 * t;
                  const edgeAngle = Math.atan2(y2 - y1, x2 - x1);
                  // Spray outwards from edge
                  const sprayAngle = edgeAngle + (Math.random() > 0.5 ? Math.PI / 2 : -Math.PI / 2) + (Math.random() - 0.5) * 0.8;
                  const speed = 2.0 + Math.random() * 4.5 * hex.energy;

                  sparks.push({
                    x: sx,
                    y: sy,
                    vx: Math.cos(sprayAngle) * speed,
                    vy: Math.sin(sprayAngle) * speed,
                    life: 1.0,
                    decay: 0.028 + Math.random() * 0.038,
                    size: 1.5 + Math.random() * 2.0,
                    length: 2.5 + Math.random() * 3.5,
                    color: Math.random() > 0.4 ? "#00f0ff" : (Math.random() > 0.5 ? "#ffffff" : "#7df9ff")
                  });
                }
              }
            }

            // Glowing white lightning vertex nodes & apex sparks
            if (hex.energy > 0.38) {
              for (let v = 0; v < 6; v++) {
                const vx = hex.cx + baseVertices[v].x;
                const vy = hex.cy + baseVertices[v].y;

                if (Math.random() < 0.5) {
                  ctx.beginPath();
                  ctx.arc(vx, vy, 2.4 * hex.energy, 0, Math.PI * 2);
                  ctx.fillStyle = "#ffffff";
                  ctx.shadowColor = "#00f0ff";
                  ctx.shadowBlur = 20;
                  ctx.fill();

                  // Vertex spark burst
                  if (Math.random() < 0.25 && sparks.length < 140) {
                    const sparkAngle = Math.random() * Math.PI * 2;
                    const spd = 2.5 + Math.random() * 4.0;
                    sparks.push({
                      x: vx,
                      y: vy,
                      vx: Math.cos(sparkAngle) * spd,
                      vy: Math.sin(sparkAngle) * spd,
                      life: 1.0,
                      decay: 0.03 + Math.random() * 0.04,
                      size: 1.8 + Math.random() * 1.6,
                      length: 3.0 + Math.random() * 4.0,
                      color: "#ffffff"
                    });
                  }
                }
              }
            }
          }
        }
      }

      // -----------------------------------------------------
      // Pass 4: Update & Render Electric Plasma Sparks (With Motion Streaks)
      // -----------------------------------------------------
      for (let s = sparks.length - 1; s >= 0; s--) {
        const p = sparks[s];
        const prevX = p.x;
        const prevY = p.y;

        p.x += p.vx;
        p.y += p.vy;
        p.vx *= 0.94;
        p.vy *= 0.94;
        p.life -= p.decay;

        if (p.life <= 0) {
          sparks.splice(s, 1);
          continue;
        }

        // High-velocity electric spark streak
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x - p.vx * p.length * p.life, p.y - p.vy * p.length * p.life);
        ctx.strokeStyle = p.color;
        ctx.lineWidth = p.size * p.life;
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 12 * p.life;
        ctx.stroke();

        // Intense bright tip
        ctx.beginPath();
        ctx.arc(p.x, p.y, (p.size * 0.8) * p.life, 0, Math.PI * 2);
        ctx.fillStyle = "#ffffff";
        ctx.shadowColor = "#ffffff";
        ctx.shadowBlur = 10 * p.life;
        ctx.fill();
      }

      requestAnimationFrame(renderHexagonEngine);
    }

    requestAnimationFrame(renderHexagonEngine);
  }

  // =========================================
  // 1. Tab Switching
  // =========================================
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      tabPanels.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const target = btn.getAttribute("data-target");
      const panel = document.getElementById(target);
      if (panel) panel.classList.add("active");
    });
  });

  // =========================================
  // 2. Segmented Buttons Component
  // =========================================
  function setupSegmented(containerId, hiddenInputId) {
    const container = document.getElementById(containerId);
    const hiddenInput = document.getElementById(hiddenInputId);
    if (!container || !hiddenInput) return;

    const buttons = container.querySelectorAll(".segmented-btn");
    buttons.forEach(btn => {
      btn.addEventListener("click", () => {
        buttons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        hiddenInput.value = btn.getAttribute("data-val");
      });
    });
  }

  function setSegmentedValue(containerId, hiddenInputId, val) {
    const container = document.getElementById(containerId);
    const hiddenInput = document.getElementById(hiddenInputId);
    if (!container || !hiddenInput) return;

    hiddenInput.value = val;
    const buttons = container.querySelectorAll(".segmented-btn");
    buttons.forEach(btn => {
      if (btn.getAttribute("data-val") === val) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });
  }

  setupSegmented("contract-segmented", "Contract");
  setupSegmented("internet-segmented", "InternetType");
  setupSegmented("payment-segmented", "PaymentMethod");

  // =========================================
  // 3. Star Rating Component
  // =========================================
  const satisfactionLabels = {
    1: "1 / 5 - Highly Dissatisfied 😡",
    2: "2 / 5 - Dissatisfied 😟",
    3: "3 / 5 - Neutral 😐",
    4: "4 / 5 - Satisfied 😊",
    5: "5 / 5 - Very Satisfied 😍"
  };

  const satisfactionContainer = document.getElementById("satisfaction-rating");
  const satisfactionInput = document.getElementById("SatisfactionScore");
  const satisfactionText = document.getElementById("satisfaction-text");

  function setSatisfaction(score) {
    if (!satisfactionInput) return;
    satisfactionInput.value = score;
    if (satisfactionText) satisfactionText.textContent = satisfactionLabels[score] || `${score} / 5`;

    if (satisfactionContainer) {
      const stars = satisfactionContainer.querySelectorAll(".rating-star-btn");
      stars.forEach(s => {
        const starScore = Number(s.getAttribute("data-score"));
        if (starScore === Number(score)) {
          s.classList.add("active");
        } else {
          s.classList.remove("active");
        }
      });
    }
  }

  satisfactionContainer?.querySelectorAll(".rating-star-btn").forEach(star => {
    star.addEventListener("click", () => {
      const score = Number(star.getAttribute("data-score"));
      setSatisfaction(score);
    });
  });

  // =========================================
  // 4. Linked Sliders & Inputs
  // =========================================
  const tenureRange = document.getElementById("tenure-range");
  const tenureInput = document.getElementById("TenureinMonths");
  const monthlyRange = document.getElementById("monthly-range");
  const monthlyInput = document.getElementById("MonthlyCharge");
  const totalInput = document.getElementById("TotalCharges");

  function autoCalcTotal() {
    const tenure = parseFloat(tenureInput?.value) || 1;
    const monthly = parseFloat(monthlyInput?.value) || 0;
    if (totalInput) {
      totalInput.value = (tenure * monthly).toFixed(2);
    }
  }

  tenureRange?.addEventListener("input", (e) => {
    if (tenureInput) tenureInput.value = e.target.value;
    autoCalcTotal();
  });

  tenureInput?.addEventListener("input", (e) => {
    if (tenureRange) tenureRange.value = e.target.value;
    autoCalcTotal();
  });

  monthlyRange?.addEventListener("input", (e) => {
    if (monthlyInput) monthlyInput.value = e.target.value;
    autoCalcTotal();
  });

  monthlyInput?.addEventListener("input", (e) => {
    if (monthlyRange) monthlyRange.value = e.target.value;
    autoCalcTotal();
  });

  // =========================================
  // 5. Presets
  // =========================================
  const presets = {
    highRisk: {
      Contract: "Month-to-Month",
      SatisfactionScore: 1,
      TenureinMonths: 2,
      MonthlyCharge: 92.5,
      InternetType: "Fiber Optic",
      PaymentMethod: "Bank Withdrawal"
    },
    loyal: {
      Contract: "Two Year",
      SatisfactionScore: 5,
      TenureinMonths: 48,
      MonthlyCharge: 65.0,
      InternetType: "DSL",
      PaymentMethod: "Credit Card"
    },
    newCustomer: {
      Contract: "One Year",
      SatisfactionScore: 4,
      TenureinMonths: 6,
      MonthlyCharge: 75.0,
      InternetType: "Cable",
      PaymentMethod: "Credit Card"
    }
  };

  function applyPreset(data) {
    if (data.Contract) setSegmentedValue("contract-segmented", "Contract", data.Contract);
    if (data.InternetType) setSegmentedValue("internet-segmented", "InternetType", data.InternetType);
    if (data.PaymentMethod) setSegmentedValue("payment-segmented", "PaymentMethod", data.PaymentMethod);
    if (data.SatisfactionScore) setSatisfaction(data.SatisfactionScore);

    if (data.TenureinMonths !== undefined) {
      if (tenureInput) tenureInput.value = data.TenureinMonths;
      if (tenureRange) tenureRange.value = data.TenureinMonths;
    }
    if (data.MonthlyCharge !== undefined) {
      if (monthlyInput) monthlyInput.value = data.MonthlyCharge;
      if (monthlyRange) monthlyRange.value = data.MonthlyCharge;
    }
    autoCalcTotal();
  }

  document.getElementById("preset-high-risk")?.addEventListener("click", () => applyPreset(presets.highRisk));
  document.getElementById("preset-loyal")?.addEventListener("click", () => applyPreset(presets.loyal));
  document.getElementById("preset-new")?.addEventListener("click", () => applyPreset(presets.newCustomer));
  document.getElementById("preset-reset")?.addEventListener("click", () => {
    applyPreset({
      Contract: "Month-to-Month",
      SatisfactionScore: 3,
      TenureinMonths: 12,
      MonthlyCharge: 70.0,
      InternetType: "Fiber Optic",
      PaymentMethod: "Bank Withdrawal"
    });
  });

  // =========================================
  // 6. Form Submission & Animation
  // =========================================
  const form = document.getElementById("prediction-form");
  form?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById("btn-predict");
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = `<span class="spinner"></span> Predicting...`;
    submitBtn.disabled = true;

    try {
      const payload = {
        Contract: document.getElementById("Contract").value,
        SatisfactionScore: Number(document.getElementById("SatisfactionScore").value),
        TenureinMonths: Number(document.getElementById("TenureinMonths").value),
        MonthlyCharge: Number(document.getElementById("MonthlyCharge").value),
        TotalCharges: Number(document.getElementById("TotalCharges").value),
        InternetType: document.getElementById("InternetType").value,
        PaymentMethod: document.getElementById("PaymentMethod").value
      };

      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Prediction request failed");
      }

      const result = await response.json();
      displayResult(result, payload);

    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });

  // =========================================
  // 7. Render Results with Animated Counter & Signals
  // =========================================
  function displayResult(result, inputData) {
    document.getElementById("results-placeholder").style.display = "none";
    const content = document.getElementById("results-content");
    content.style.display = "flex";

    const hero = document.getElementById("verdict-hero");
    const title = document.getElementById("verdict-title");
    const sub = document.getElementById("verdict-sub");
    const badge = document.getElementById("verdict-badge");
    const meterFill = document.getElementById("meter-bar-fill");
    const meterNum = document.getElementById("churn-percent-num");
    const signalsList = document.getElementById("risk-signals-list");
    const actionsList = document.getElementById("action-plan-list");

    const isChurn = result.prediction === 1;
    const targetProb = result.churn_probability;

    animateNumber(meterNum, 0, targetProb, 800, "%");
    meterFill.style.width = `${targetProb}%`;

    if (isChurn) {
      hero.className = "verdict-hero churn";
      title.className = "verdict-big-title churn";
      title.textContent = "High Churn Risk 🚨";
      sub.textContent = "High probability of customer leaving the service";
      badge.className = "verdict-badge high";
      badge.textContent = `${result.risk_level.toUpperCase()} RISK`;
      meterFill.style.background = "var(--neon-rose)";
    } else {
      hero.className = "verdict-hero stay";
      title.className = "verdict-big-title stay";
      title.textContent = "Customer Likely to Stay 🛡️";
      sub.textContent = "Customer profile shows strong loyalty indicators";
      badge.className = "verdict-badge low";
      badge.textContent = `${result.risk_level.toUpperCase()} RISK`;
      meterFill.style.background = "var(--neon-cyan)";
    }

    signalsList.innerHTML = "";
    const signals = [];

    if (inputData.SatisfactionScore <= 2) {
      signals.push(`🔴 <strong>Low Satisfaction Score (${inputData.SatisfactionScore}/5):</strong> Strong negative sentiment.`);
    } else if (inputData.SatisfactionScore >= 4) {
      signals.push(`🟢 <strong>High Satisfaction Score (${inputData.SatisfactionScore}/5):</strong> Customer feels well-served.`);
    }

    if (inputData.Contract === "Month-to-Month") {
      signals.push(`🔴 <strong>Month-to-Month Agreement:</strong> Zero lock-in creates high churn vulnerability.`);
    } else {
      signals.push(`🟢 <strong>Committed Contract (${inputData.Contract}):</strong> Contract duration strongly stabilizes customer relationship.`);
    }

    if (inputData.TenureinMonths <= 6) {
      signals.push(`🟡 <strong>Early Stage (< 6 months):</strong> Fragile customer onboarding period.`);
    } else if (inputData.TenureinMonths >= 24) {
      signals.push(`🟢 <strong>Long-Term Customer (${inputData.TenureinMonths} mos):</strong> Proven product loyalty.`);
    }

    if (inputData.MonthlyCharge >= 85) {
      signals.push(`🟡 <strong>High Monthly Spend ($${inputData.MonthlyCharge}):</strong> High sensitivity to competitor discounts.`);
    }

    signals.forEach(s => {
      const li = document.createElement("li");
      li.innerHTML = s;
      signalsList.appendChild(li);
    });

    actionsList.innerHTML = "";
    const actions = [];
    if (isChurn) {
      actions.push(`📞 <strong>Proactive Outreach:</strong> Contact customer within 24 hours to address satisfaction.`);
      actions.push(`🎁 <strong>Contract Incentive:</strong> Offer a 15% discount on switching to a 1-year agreement.`);
    } else {
      actions.push(`✨ <strong>Loyalty Engagement:</strong> Send satisfaction appreciation perks or rewards.`);
      actions.push(`🚀 <strong>Upsell Opportunity:</strong> Profile qualifies for speed upgrade or family bundles.`);
    }

    actions.forEach(a => {
      const li = document.createElement("li");
      li.innerHTML = a;
      actionsList.appendChild(li);
    });
  }

  function animateNumber(element, start, end, duration, suffix = "") {
    const startTime = performance.now();
    function update(time) {
      const elapsed = time - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const current = (start + (end - start) * progress).toFixed(1);
      element.textContent = `${current}${suffix}`;
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.textContent = `${end.toFixed(1)}${suffix}`;
      }
    }
    requestAnimationFrame(update);
  }



  // =========================================
  // 9. Load Metrics
  // =========================================
  async function loadMetrics() {
    try {
      const res = await fetch("/api/metrics");
      if (res.ok) {
        const m = await res.json();
        if (m.accuracy) document.getElementById("val-accuracy").textContent = (m.accuracy * 100).toFixed(2) + "%";
        if (m.precision) document.getElementById("val-precision").textContent = (m.precision * 100).toFixed(2) + "%";
        if (m.recall) document.getElementById("val-recall").textContent = (m.recall * 100).toFixed(2) + "%";
        if (m.F1_score) document.getElementById("val-f1").textContent = (m.F1_score * 100).toFixed(2) + "%";
      }
    } catch (e) {}
  }
  document.getElementById("btn-refresh-metrics")?.addEventListener("click", loadMetrics);
  loadMetrics();

});
