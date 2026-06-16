/* 台股千金俄羅斯輪盤 · 黑猩猩射飛鏢
 * 隨機選股遊戲，落點後放大顯示股名與建議購買股數 5 秒。
 * 純屬娛樂模擬，不構成投資建議。
 */
(() => {
  "use strict";

  const canvas = document.getElementById("wheel");
  const ctx = canvas.getContext("2d");
  const spinBtn = document.getElementById("spinBtn");
  const pointer = document.getElementById("pointer");
  const soundToggle = document.getElementById("soundToggle");
  const historyList = document.getElementById("historyList");

  const reveal = document.getElementById("reveal");
  const revealName = document.getElementById("revealName");
  const revealCode = document.getElementById("revealCode");
  const revealShares = document.getElementById("revealShares");
  const revealCount = document.getElementById("revealCount");
  const confetti = document.getElementById("confetti");

  const N = STOCKS.length;
  const SEG = (Math.PI * 2) / N;       // 每格弧度
  const R = canvas.width / 2;
  const TAU = Math.PI * 2;

  let rotation = 0;        // 目前輪盤角度（弧度）
  let spinning = false;
  let soundOn = true;

  /* ---------- 音效（Web Audio，免外部檔案） ---------- */
  let audioCtx = null;
  function ac() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") audioCtx.resume();
    return audioCtx;
  }
  function tone(freq, dur, type = "sine", gain = 0.2, delay = 0) {
    if (!soundOn) return;
    const c = ac();
    const t = c.currentTime + delay;
    const osc = c.createOscillator();
    const g = c.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g).connect(c.destination);
    osc.start(t);
    osc.stop(t + dur + 0.02);
  }
  // 經過卡榫的「噠」聲
  function tick() {
    if (!soundOn) return;
    tone(880, 0.04, "square", 0.08);
  }
  // 飛鏢射出「咻」聲
  function whoosh() {
    if (!soundOn) return;
    const c = ac();
    const t = c.currentTime;
    const osc = c.createOscillator();
    const g = c.createGain();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(1200, t);
    osc.frequency.exponentialRampToValueAtTime(200, t + 0.35);
    g.gain.setValueAtTime(0.18, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.35);
    osc.connect(g).connect(c.destination);
    osc.start(t);
    osc.stop(t + 0.37);
  }
  // 命中號角聲
  function fanfare() {
    if (!soundOn) return;
    const seq = [523.25, 659.25, 783.99, 1046.5];
    seq.forEach((f, i) => tone(f, 0.28, "triangle", 0.22, i * 0.12));
    tone(1318.5, 0.5, "sine", 0.18, seq.length * 0.12);
  }

  /* ---------- 繪製輪盤 ---------- */
  function drawWheel() {
    ctx.clearRect(0, 0, canvas.width, canvas.width);
    ctx.save();
    ctx.translate(R, R);
    ctx.rotate(rotation);

    for (let i = 0; i < N; i++) {
      const a0 = i * SEG;
      const a1 = a0 + SEG;
      // 色塊
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.arc(0, 0, R - 6, a0, a1);
      ctx.closePath();
      ctx.fillStyle = STOCKS[i].color;
      ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = "rgba(255,255,255,0.25)";
      ctx.stroke();

      // 文字
      ctx.save();
      ctx.rotate(a0 + SEG / 2);
      ctx.textAlign = "right";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#ffffff";
      ctx.shadowColor = "rgba(0,0,0,0.55)";
      ctx.shadowBlur = 4;
      const label = STOCKS[i].name;
      ctx.font = `700 ${label.length > 4 ? 14 : 17}px "Noto Sans TC","Microsoft JhengHei",sans-serif`;
      ctx.fillText(label, R - 20, 0);
      ctx.restore();
    }

    // 中心圓
    ctx.beginPath();
    ctx.arc(0, 0, R * 0.16, 0, TAU);
    ctx.fillStyle = "#1a1730";
    ctx.fill();
    ctx.restore();
  }

  /* ---------- 命中判定 ---------- */
  // 指針在正上方（-90°）。換算落在哪一格。
  function indexAtPointer() {
    const pointerAngle = -Math.PI / 2;        // 正上方
    let rel = (pointerAngle - rotation) % TAU;
    if (rel < 0) rel += TAU;
    return Math.floor(rel / SEG) % N;
  }

  /* ---------- 轉動 ---------- */
  function spin() {
    if (spinning) return;
    spinning = true;
    spinBtn.disabled = true;
    canvas.classList.add("spinning");
    whoosh();

    // 隨機目標：5~8 圈 + 隨機落點，營造驚喜
    const targetIndex = Math.floor(Math.random() * N);
    const extraTurns = 5 + Math.floor(Math.random() * 4);
    // 讓 targetIndex 的中心對齊指針
    const targetCenter = targetIndex * SEG + SEG / 2;
    const finalRotation =
      extraTurns * TAU + (-Math.PI / 2 - targetCenter) - (rotation % TAU);

    const startRotation = rotation;
    const totalDelta = finalRotation;
    const duration = 4200 + Math.random() * 1200;
    const startTime = performance.now();
    let lastTickIndex = indexAtPointer();

    function easeOutQuart(t) { return 1 - Math.pow(1 - t, 4); }

    function frame(now) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      rotation = startRotation + totalDelta * easeOutQuart(t);
      drawWheel();

      // 經過卡榫時發出噠聲
      const idx = indexAtPointer();
      if (idx !== lastTickIndex) {
        tick();
        lastTickIndex = idx;
      }

      if (t < 1) {
        requestAnimationFrame(frame);
      } else {
        spinning = false;
        canvas.classList.remove("spinning");
        finishSpin();
      }
    }
    requestAnimationFrame(frame);
  }

  function finishSpin() {
    const idx = indexAtPointer();
    const stock = STOCKS[idx];
    const shares = 1 + Math.floor(Math.random() * 10);   // 1~10 股

    pointer.classList.add("hit");
    setTimeout(() => pointer.classList.remove("hit"), 400);
    fanfare();

    showReveal(stock, shares);
    addHistory(stock, shares);
  }

  /* ---------- 落點放大顯示（5 秒） ---------- */
  let revealTimer = null;
  let countdownTimer = null;
  function showReveal(stock, shares) {
    revealName.textContent = stock.name;
    revealCode.textContent = stock.code.replace(/[a-z]/g, "");  // 去掉內部去重後綴
    revealShares.textContent = shares;
    reveal.classList.add("show");
    reveal.setAttribute("aria-hidden", "false");
    launchConfetti();

    let left = 5;
    revealCount.textContent = left;
    clearInterval(countdownTimer);
    countdownTimer = setInterval(() => {
      left -= 1;
      revealCount.textContent = left;
      if (left <= 0) clearInterval(countdownTimer);
    }, 1000);

    clearTimeout(revealTimer);
    revealTimer = setTimeout(closeReveal, 5000);
  }

  function closeReveal() {
    reveal.classList.remove("show");
    reveal.setAttribute("aria-hidden", "true");
    confetti.innerHTML = "";
    spinBtn.disabled = false;
  }

  /* ---------- 彩帶 ---------- */
  function launchConfetti() {
    confetti.innerHTML = "";
    const colors = ["#ffd54a", "#ff6b6b", "#4ecdc4", "#a29bfe", "#1dd1a1", "#feca57"];
    for (let i = 0; i < 80; i++) {
      const s = document.createElement("span");
      s.style.left = Math.random() * 100 + "vw";
      s.style.background = colors[i % colors.length];
      s.style.animationDuration = 2 + Math.random() * 2 + "s";
      s.style.animationDelay = Math.random() * 0.6 + "s";
      s.style.transform = `rotate(${Math.random() * 360}deg)`;
      confetti.appendChild(s);
    }
  }

  /* ---------- 歷史紀錄 ---------- */
  function addHistory(stock, shares) {
    const li = document.createElement("li");
    li.innerHTML =
      `<span class="h-name">${stock.name} (${stock.code.replace(/[a-z]/g, "")})</span>` +
      `<span class="h-shares">${shares} 股</span>`;
    historyList.prepend(li);
    while (historyList.children.length > 12) historyList.lastChild.remove();
  }

  /* ---------- 事件 ---------- */
  spinBtn.addEventListener("click", () => { ac(); spin(); });
  soundToggle.addEventListener("click", () => {
    soundOn = !soundOn;
    soundToggle.textContent = soundOn ? "🔊 音效：開" : "🔇 音效：關";
  });
  // 點背景可提早關閉放大畫面
  reveal.addEventListener("click", () => {
    clearTimeout(revealTimer);
    clearInterval(countdownTimer);
    closeReveal();
  });

  drawWheel();
})();
