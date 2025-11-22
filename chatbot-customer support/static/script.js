function sendMessage() {
    const inputBox = document.getElementById("userInput");
    const message = inputBox.value;
    if(message.trim() === "") return;

    addMessage(message, "user-msg");
    inputBox.value = "";
    showTypingIndicator();

    fetch("/get_response", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator();
        addMessage(data.response, "bot-msg");
    });
}

function addMessage(message, className) {
    const chatbox = document.getElementById("chatbox");
    const msgDiv = document.createElement("div");
    msgDiv.className = "message " + className;
    msgDiv.innerText = message;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function showTypingIndicator() {
    const chatbox = document.getElementById("chatbox");
    const typingIndicator = document.querySelector(".bot-typing-indicator");
    typingIndicator.style.display = "flex";
    chatbox.scrollTop = chatbox.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.querySelector(".bot-typing-indicator");
    typingIndicator.style.display = "none";
}