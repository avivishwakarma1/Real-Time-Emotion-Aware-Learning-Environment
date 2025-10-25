const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const userIdInput = document.getElementById("userId");
const roleSelect = document.getElementById("role");
const intervalInput = document.getElementById("interval");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const lastEmotion = document.getElementById("lastEmotion");
const lastConf = document.getElementById("lastConf");
const lastEng = document.getElementById("lastEng");

let stream = null;
let timer = null;

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    await video.play();
    canvas.width = 320;
    canvas.height = 240;
    console.log("Camera started successfully.");
    return true; // Indicate success
  } catch (err) {
    console.error("Camera error:", err);
    alert("Could not access camera. Please check browser settings and allow permission.");
    return false; // Indicate failure
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(t => t.stop());
    stream = null;
    console.log("Camera stopped.");
  }
}

async function captureAndSend() {
  if (!stream) return;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.7);
  const payload = {
    image: dataUrl,
    user_id: (userIdInput.value || "anonymous").trim(),
    role: roleSelect.value
  };
  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const j = await res.json();
    if (j.status === "ok") {
      lastEmotion.innerText = j.emotion;
      lastConf.innerText = (j.confidence || 0).toFixed(2);
      lastEng.innerText = (j.engagement || 0).toFixed(2);
    } else {
      console.warn("Server error:", j);
    }
  } catch (err) {
    console.error("Error sending frame:", err);
  }
}

function startCapturing() {
  if (!stream) return;
  captureAndSend();
  const intervalSec = Math.max(1, parseInt(intervalInput.value || "3", 10));
  timer = setInterval(captureAndSend, intervalSec * 1000);
}

function stopCapturing() {
  if (timer) clearInterval(timer);
  timer = null;
}

startBtn.addEventListener("click", async () => {
  startBtn.disabled = true;
  stopBtn.disabled = false;
  await startCamera();
  startCapturing();
});

stopBtn.addEventListener("click", () => {
  startBtn.disabled = false;
  stopBtn.disabled = true;
  stopCapturing();
  stopCamera();
});

// Auto-start camera and capturing when page loads
window.addEventListener("load", async () => {
  const cameraStarted = await startCamera();
  if (cameraStarted) {
    startCapturing();
    startBtn.disabled = true;
    stopBtn.disabled = false;
  } else {
    // If camera fails on load, ensure the start button is enabled to let the user try again
    startBtn.disabled = false;
    stopBtn.disabled = true;
  }
});