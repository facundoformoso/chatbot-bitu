[23:08, 3/11/2025] formoso: 3-document.addEventListener("DOMContentLoaded", function(){
  const btn = document.getElementById("bitu-chat-button");
  const modal = document.getElementById("bitu-chat-modal");
  const closeBtn = document.getElementById("bitu-close");
  const form = document.getElementById("bitu-form");
  const input = document.getElementById("bitu-input");
  const messages = document.getElementById("bitu-messages");

  function openModal(){
    modal.style.display = "flex";
    input.focus();
  }
  function closeModal(){
    modal.style.display = "none";
  }

  btn.addEventListener("click", openModal);
  closeBtn.addEventListener("click", closeModal);

  // helper to add message
  function addMessage(text, sender){
    const wrapper = document.createElement("div");
    wr…
[23:09, 3/11/2025] formoso: const bubble = document.getElementById("bitu-bubble");
const chat = document.getElementById("bitu-chat");
const messages = document.getElementById("bitu-messages");
const input = document.getElementById("bitu-user-input");
const send = document.getElementById("bitu-send");

// Alternar visibilidad del chat
bubble.onclick = () => {
  chat.style.display = chat.style.display === "flex" ? "none" : "flex";
};

// Enviar mensaje
send.onclick = async () => {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "bitu-user");
  input.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    const reply = data.reply || 
      "Nuestro equipo de IA no tiene la respuesta a esta pregunta por ahora. Pero no te preocupes, puedes contactarte con nuestro equipo al +54 9 11 5185-7753.";
    addMessage(reply, "bitu-bot");
  } catch (err) {
    addMessage("Hubo un error al conectar con el servidor. Intenta nuevamente más tarde.", "bitu-bot");
  }
};

function addMessage(text, cls) {
  const msg = document.createElement("div");
  msg.className = "bitu-message " + cls;
  msg.textContent = text;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
}

// Enter para enviar
input.addEventListener("keypress", e => {
  if (e.key === "Enter") send.click();
});
