document.addEventListener("DOMContentLoaded", () => {

  // ═══════════════════════════════════════════════════════════
  // 0. LIGHTNING CANVAS — Electric Hex Grid with Mouse Effect
  // ═══════════════════════════════════════════════════════════
  const canvas = document.getElementById("lightning-canvas");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    let W = 0, H = 0, dpr = devicePixelRatio || 1;
    let mouseX = -9999, mouseY = -9999, onScreen = false;

    const HEX_R    = 34;
    const HEX_W    = Math.sqrt(3) * HEX_R;
    const HEX_H    = 1.5 * HEX_R;
    const HOVER_R  = 200;

    // Pre-build pointy-top hex vertices
    const BASE_V = Array.from({length:6}, (_,i) => {
      const a = Math.PI/6 + i*Math.PI/3;
      return { x: HEX_R * Math.cos(a), y: HEX_R * Math.sin(a) };
    });

    let hexes = [];

    function buildGrid() {
      dpr = devicePixelRatio || 1;
      W = window.innerWidth; H = window.innerHeight;
      canvas.width  = Math.floor(W * dpr);
      canvas.height = Math.floor(H * dpr);
      canvas.style.width  = W + "px";
      canvas.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      hexes = [];
      const cols = Math.ceil(W / HEX_W) + 3;
      const rows = Math.ceil(H / HEX_H) + 3;
      for (let r = -1; r < rows; r++) {
        const odd = (r & 1) === 1;
        for (let c = -1; c < cols; c++) {
          hexes.push({
            cx: c * HEX_W + (odd ? HEX_W / 2 : 0),
            cy: r * HEX_H,
            e: 0
          });
        }
      }
    }

    window.addEventListener("resize",    buildGrid);
    window.addEventListener("mousemove", e => { mouseX = e.clientX; mouseY = e.clientY; onScreen = true; });
    window.addEventListener("mouseenter",e => { mouseX = e.clientX; mouseY = e.clientY; onScreen = true; });
    window.addEventListener("mouseleave",() => { onScreen = false; mouseX = -9999; mouseY = -9999; });
    buildGrid();

    // Draw a jagged electric bolt between two points
    function bolt(x1, y1, x2, y2, intensity, color) {
      const dx = x2-x1, dy = y2-y1;
      const len = Math.hypot(dx, dy);
      if (len < 1) return;
      const px = -dy/len, py = dx/len;
      const steps = 5;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      for (let s = 1; s < steps; s++) {
        const t = s / steps;
        const j = (Math.random() - 0.5) * 5.5 * intensity;
        ctx.lineTo(x1 + dx*t + px*j, y1 + dy*t + py*j);
      }
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = color;
      ctx.lineWidth   = 1.2 + intensity * 2.0;
      ctx.shadowColor = "#0077fe";
      ctx.shadowBlur  = 12 * intensity;
      ctx.stroke();
      // White-hot core
      if (intensity > 0.42) {
        ctx.beginPath();
        ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
        ctx.strokeStyle = `rgba(255,255,255,${Math.min((intensity-0.42)*2.4,1)})`;
        ctx.lineWidth   = 1.0;
        ctx.shadowColor = "#ffffff";
        ctx.shadowBlur  = 8;
        ctx.stroke();
      }
    }

    let lastT = performance.now();

    function frame(ts) {
      ctx.clearRect(0, 0, W, H);
      ctx.shadowBlur = 0;

      const active = [];

      // Energy update
      for (const h of hexes) {
        if (onScreen) {
          const d = Math.hypot(h.cx - mouseX, h.cy - mouseY);
          if (d < HOVER_R) h.e = Math.max(h.e, Math.pow(1 - d/HOVER_R, 1.7));
        }
        h.e *= 0.88;
        if (h.e < 0.004) h.e = 0;
        if (h.e > 0.008) active.push(h);
      }

      // ── Pass 1: faint blue lattice (always visible) ──
      ctx.beginPath();
      ctx.lineWidth   = 0.7;
      ctx.strokeStyle = "rgba(0,102,255,0.10)";
      ctx.shadowBlur  = 0;
      for (const h of hexes) {
        for (let v = 0; v < 6; v++) {
          const vx = h.cx + BASE_V[v].x, vy = h.cy + BASE_V[v].y;
          v === 0 ? ctx.moveTo(vx,vy) : ctx.lineTo(vx,vy);
        }
        ctx.closePath();
      }
      ctx.stroke();

      // Subtle corner dots
      ctx.fillStyle = "rgba(0,102,255,0.18)";
      for (let i = 0; i < hexes.length; i+=2) {
        const h = hexes[i];
        for (const v of BASE_V) ctx.fillRect(h.cx+v.x-0.8, h.cy+v.y-0.8, 1.6, 1.6);
      }

      // ── Pass 2: glowing borders on hover ──
      for (const h of active) {
        ctx.beginPath();
        for (let v = 0; v < 6; v++) {
          const vx = h.cx + BASE_V[v].x, vy = h.cy + BASE_V[v].y;
          v===0 ? ctx.moveTo(vx,vy) : ctx.lineTo(vx,vy);
        }
        ctx.closePath();
        ctx.strokeStyle = `rgba(0,119,254,${Math.min(0.25+h.e*0.75,0.95)})`;
        ctx.lineWidth   = 1.0 + h.e * 2.2;
        ctx.shadowColor = "#00a6f4";
        ctx.shadowBlur  = h.e * 18;
        ctx.stroke();
        if (h.e > 0.5) {
          ctx.strokeStyle = `rgba(255,255,255,${(h.e-0.5)*1.6})`;
          ctx.lineWidth   = 1.1;
          ctx.shadowColor = "#ffffff";
          ctx.shadowBlur  = 10;
          ctx.stroke();
        }
      }

      // ── Pass 3: electric lightning surges ──
      ctx.shadowBlur = 0;
      for (const h of active) {
        if (h.e < 0.22) continue;
        for (let e = 0; e < 6; e++) {
          const v1 = BASE_V[e], v2 = BASE_V[(e+1)%6];
          if (Math.random() < h.e * 0.72) {
            bolt(
              h.cx+v1.x, h.cy+v1.y,
              h.cx+v2.x, h.cy+v2.y,
              h.e,
              `rgba(0,166,244,${Math.min(h.e*1.4,1)})`
            );
          }
        }
        // Glowing nodes
        if (h.e > 0.36) {
          for (const v of BASE_V) {
            if (Math.random() < 0.42) {
              ctx.beginPath();
              ctx.arc(h.cx+v.x, h.cy+v.y, 2.4*h.e, 0, Math.PI*2);
              ctx.fillStyle   = "#ffffff";
              ctx.shadowColor = "#00a6f4";
              ctx.shadowBlur  = 16;
              ctx.fill();
            }
          }
          ctx.shadowBlur = 0;
        }
      }

      lastT = ts;
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  // ═══════════════════════════════════════════════════════════
  // 1. TAB SWITCHING
  // ═══════════════════════════════════════════════════════════
  document.querySelectorAll(".nav-tab").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".nav-tab").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const panel = document.getElementById(btn.getAttribute("data-target"));
      if (panel) panel.classList.add("active");
    });
  });

  // ═══════════════════════════════════════════════════════════
  // 2. SEGMENTED BUTTONS
  // ═══════════════════════════════════════════════════════════
  function setupSeg(groupId, hiddenId) {
    const grp = document.getElementById(groupId);
    const hid = document.getElementById(hiddenId);
    if (!grp || !hid) return;
    grp.querySelectorAll(".seg-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        grp.querySelectorAll(".seg-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        hid.value = btn.dataset.val;
      });
    });
  }
  function setSegVal(groupId, hiddenId, val) {
    const grp = document.getElementById(groupId);
    const hid = document.getElementById(hiddenId);
    if (!grp || !hid) return;
    hid.value = val;
    grp.querySelectorAll(".seg-btn").forEach(b =>
      b.classList.toggle("active", b.dataset.val === val)
    );
  }
  setupSeg("contract-segmented",  "Contract");
  setupSeg("internet-segmented",  "InternetType");
  setupSeg("payment-segmented",   "PaymentMethod");

  // ═══════════════════════════════════════════════════════════
  // 3. STAR RATING
  // ═══════════════════════════════════════════════════════════
  const SAT_LABELS = {1:"1/5 – Highly Dissatisfied 😡",2:"2/5 – Dissatisfied 😟",3:"3/5 – Neutral 😐",4:"4/5 – Satisfied 😊",5:"5/5 – Very Satisfied 😍"};
  const satInput = document.getElementById("SatisfactionScore");
  const satText  = document.getElementById("satisfaction-text");
  const satGrp   = document.getElementById("satisfaction-rating");

  function setSat(score) {
    if (!satInput) return;
    satInput.value = score;
    if (satText) satText.textContent = SAT_LABELS[score] || score + "/5";
    satGrp?.querySelectorAll(".star-btn").forEach(b =>
      b.classList.toggle("active", Number(b.dataset.score) === Number(score))
    );
  }
  satGrp?.querySelectorAll(".star-btn").forEach(b =>
    b.addEventListener("click", () => setSat(Number(b.dataset.score)))
  );

  // ═══════════════════════════════════════════════════════════
  // 4. LINKED SLIDERS
  // ═══════════════════════════════════════════════════════════
  const tenureRange  = document.getElementById("tenure-range");
  const tenureInput  = document.getElementById("TenureinMonths");
  const monthlyRange = document.getElementById("monthly-range");
  const monthlyInput = document.getElementById("MonthlyCharge");
  const totalInput   = document.getElementById("TotalCharges");

  function calcTotal() {
    const t = parseFloat(tenureInput?.value)  || 1;
    const m = parseFloat(monthlyInput?.value) || 0;
    if (totalInput) totalInput.value = (t * m).toFixed(2);
  }
  tenureRange?.addEventListener("input",  e => { if(tenureInput)  tenureInput.value  = e.target.value; calcTotal(); });
  tenureInput?.addEventListener("input",  e => { if(tenureRange)  tenureRange.value  = e.target.value; calcTotal(); });
  monthlyRange?.addEventListener("input", e => { if(monthlyInput) monthlyInput.value = e.target.value; calcTotal(); });
  monthlyInput?.addEventListener("input", e => { if(monthlyRange) monthlyRange.value = e.target.value; calcTotal(); });

  // ═══════════════════════════════════════════════════════════
  // 5. PRESETS
  // ═══════════════════════════════════════════════════════════
  function applyPreset(d) {
    if (d.Contract)       setSegVal("contract-segmented","Contract",d.Contract);
    if (d.InternetType)   setSegVal("internet-segmented","InternetType",d.InternetType);
    if (d.PaymentMethod)  setSegVal("payment-segmented","PaymentMethod",d.PaymentMethod);
    if (d.SatisfactionScore) setSat(d.SatisfactionScore);
    if (d.TenureinMonths !== undefined) {
      if (tenureInput) tenureInput.value = d.TenureinMonths;
      if (tenureRange) tenureRange.value = d.TenureinMonths;
    }
    if (d.MonthlyCharge !== undefined) {
      if (monthlyInput) monthlyInput.value = d.MonthlyCharge;
      if (monthlyRange) monthlyRange.value = d.MonthlyCharge;
    }
    calcTotal();
  }
  document.getElementById("preset-high-risk")?.addEventListener("click", () => applyPreset({Contract:"Month-to-Month",SatisfactionScore:1,TenureinMonths:2,MonthlyCharge:92.5,InternetType:"Fiber Optic",PaymentMethod:"Bank Withdrawal"}));
  document.getElementById("preset-loyal")?.addEventListener("click",     () => applyPreset({Contract:"Two Year",SatisfactionScore:5,TenureinMonths:48,MonthlyCharge:65,InternetType:"DSL",PaymentMethod:"Credit Card"}));
  document.getElementById("preset-new")?.addEventListener("click",       () => applyPreset({Contract:"One Year",SatisfactionScore:4,TenureinMonths:6,MonthlyCharge:75,InternetType:"Cable",PaymentMethod:"Credit Card"}));
  document.getElementById("preset-reset")?.addEventListener("click",     () => applyPreset({Contract:"Month-to-Month",SatisfactionScore:3,TenureinMonths:12,MonthlyCharge:70,InternetType:"Fiber Optic",PaymentMethod:"Bank Withdrawal"}));

  // ═══════════════════════════════════════════════════════════
  // 6. PREDICTION FORM
  // ═══════════════════════════════════════════════════════════
  document.getElementById("prediction-form")?.addEventListener("submit", async e => {
    e.preventDefault();
    const btn  = document.getElementById("btn-predict");
    const orig = btn.innerHTML;
    btn.innerHTML = `<span class="spinner"></span> Analyzing...`;
    btn.disabled  = true;

    try {
      const payload = {
        Contract:         document.getElementById("Contract").value,
        SatisfactionScore:Number(document.getElementById("SatisfactionScore").value),
        TenureinMonths:   Number(tenureInput.value),
        MonthlyCharge:    Number(monthlyInput.value),
        TotalCharges:     Number(totalInput.value),
        InternetType:     document.getElementById("InternetType").value,
        PaymentMethod:    document.getElementById("PaymentMethod").value
      };

      const res = await fetch("/api/predict", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Prediction failed");
      renderResult(await res.json(), payload);

    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      btn.innerHTML = orig;
      btn.disabled  = false;
    }
  });

  function renderResult(result, input) {
    document.getElementById("results-placeholder").style.display = "none";
    const content = document.getElementById("results-content");
    content.style.display = "flex";

    const isChurn = result.prediction === 1;
    const prob    = result.churn_probability;
    const risk    = result.risk_level;

    // Verdict
    const hero  = document.getElementById("verdict-hero");
    const badge = document.getElementById("verdict-badge");
    const title = document.getElementById("verdict-title");
    const sub   = document.getElementById("verdict-sub");

    hero.className     = "verdict " + (isChurn ? "churn" : "stay");
    badge.className    = "verdict-badge " + (risk==="High"?"high":risk==="Medium"?"medium":"low");
    badge.textContent  = risk.toUpperCase() + " RISK";
    title.textContent  = isChurn ? "High Churn Risk 🚨" : "Customer Likely to Stay 🛡️";
    sub.textContent    = isChurn ? "Immediate intervention recommended." : "Strong loyalty indicators detected.";

    // Gauge
    const fill = document.getElementById("meter-bar-fill");
    const num  = document.getElementById("churn-percent-num");
    fill.style.width      = prob + "%";
    fill.style.background = isChurn
      ? "linear-gradient(90deg,#f87171,#f43f5e)"
      : "linear-gradient(90deg,#34d399,#10b981)";
    animNum(num, 0, prob, 900, "%");

    // Signals
    const sigs = [];
    if (input.SatisfactionScore <= 2) sigs.push(`🔴 <strong>Low Satisfaction (${input.SatisfactionScore}/5):</strong> Strong churn signal.`);
    else if (input.SatisfactionScore >= 4) sigs.push(`🟢 <strong>High Satisfaction (${input.SatisfactionScore}/5):</strong> Customer feels valued.`);
    if (input.Contract === "Month-to-Month") sigs.push(`🔴 <strong>Month-to-Month:</strong> No lock-in — high vulnerability.`);
    else sigs.push(`🟢 <strong>${input.Contract}:</strong> Contract anchors the relationship.`);
    if (input.TenureinMonths <= 6) sigs.push(`🟡 <strong>New (${input.TenureinMonths} mo):</strong> Fragile onboarding period.`);
    else if (input.TenureinMonths >= 24) sigs.push(`🟢 <strong>Long-term (${input.TenureinMonths} mo):</strong> Proven loyalty.`);
    if (input.MonthlyCharge >= 85) sigs.push(`🟡 <strong>High Spend ($${input.MonthlyCharge}):</strong> Price-sensitive customer.`);
    document.getElementById("risk-signals-list").innerHTML = sigs.map(s=>`<li>${s}</li>`).join("");

    const acts = isChurn
      ? [`📞 <strong>Proactive Call:</strong> Reach out within 24h.`,
         `🎁 <strong>Contract Incentive:</strong> Offer 15% off a 1-year plan.`,
         `⭐ <strong>Personalised Bundle:</strong> Match an offer to their usage.`]
      : [`✨ <strong>Loyalty Reward:</strong> Send appreciation perks.`,
         `🚀 <strong>Upsell:</strong> Offer a speed upgrade or family bundle.`];
    document.getElementById("action-plan-list").innerHTML = acts.map(a=>`<li>${a}</li>`).join("");
  }

  function animNum(el, from, to, dur, suf) {
    const t0 = performance.now();
    (function step(t) {
      const p = Math.min((t-t0)/dur, 1);
      el.textContent = (from + (to-from)*p).toFixed(1) + suf;
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = to.toFixed(1) + suf;
    })(performance.now());
  }

  // ═══════════════════════════════════════════════════════════
  // 7. LOAD METRICS
  // ═══════════════════════════════════════════════════════════
  async function loadMetrics() {
    try {
      const res = await fetch("/api/metrics");
      if (!res.ok) return;
      const m = await res.json();
      if (m.accuracy)  document.getElementById("val-accuracy").textContent  = (m.accuracy*100).toFixed(2)+"%";
      if (m.precision) document.getElementById("val-precision").textContent = (m.precision*100).toFixed(2)+"%";
      if (m.recall)    document.getElementById("val-recall").textContent    = (m.recall*100).toFixed(2)+"%";
      if (m.F1_score)  document.getElementById("val-f1").textContent        = (m.F1_score*100).toFixed(2)+"%";
    } catch(e) {}
  }
  document.getElementById("btn-refresh-metrics")?.addEventListener("click", loadMetrics);
  loadMetrics();

});
