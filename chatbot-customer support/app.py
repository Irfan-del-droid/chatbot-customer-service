from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ---------------- Chatbot Logic ----------------
keywords = {
    'greeting': ['hi', 'hello', 'hey'],
    'product_info': ['product', 'feature', 'details'],
    'order_status': ['order', 'track', 'shipment'],
    'return_refund': ['return', 'refund', 'exchange'],
    'payment': ['payment', 'installment', 'pay']
}

responses = {
    'greeting': "Hello! Welcome to our support. How can I help you today?",
    'product_info': "Product X comes with A, B, and C features.",
    'order_status': "Can you provide your order ID so I can check the status?",
    'return_refund': "You can return items within 30 days. Visit our returns page.",
    'payment': "We accept credit cards, debit cards, UPI, and EMI options.",
    'fallback': "I’m sorry, I didn’t understand that. Can you rephrase?"
}

def detect_intent(user_input):
    tokens = user_input.lower().split()
    for intent, keys in keywords.items():
        if any(word in tokens for word in keys):
            return intent
    return 'fallback'

def get_bot_response(user_input):
    intent = detect_intent(user_input)
    return responses[intent]

# ---------------- Routes ----------------
@app.route("/")
def index():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Customer Support Chatbot</title>
        <style>
            /* --- General Body --- */
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to bottom, #ece9e6, #ffffff);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            /* --- Chat Container --- */
            .chat-container {
                width: 400px;
                max-width: 90%;
                background: #fff;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            /* --- Chat Header --- */
            .chat-header {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
            }

            /* --- Chat Messages --- */
            #chatbox {
                height: 350px;
                padding: 15px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 10px;
                background-color: #f5f5f5;
            }

            .message {
                max-width: 80%;
                padding: 10px 15px;
                border-radius: 20px;
                line-height: 1.4;
                word-wrap: break-word;
            }

            .user-msg {
                background-color: #DCF8C6;
                align-self: flex-end;
            }

            .bot-msg {
                background-color: #ffffff;
                align-self: flex-start;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }

            /* --- Input Area --- */
            .input-area {
                display: flex;
                padding: 10px;
                border-top: 1px solid #ccc;
                background-color: #fafafa;
            }

            #userInput {
                flex: 1;
                padding: 10px 15px;
                border: 1px solid #ccc;
                border-radius: 25px;
                outline: none;
                font-size: 14px;
            }

            #sendBtn {
                padding: 10px 20px;
                margin-left: 10px;
                border: none;
                border-radius: 25px;
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.3s;
            }

            #sendBtn:hover {
                background-color: #45a049;
            }

            /* --- Scrollbar Styling --- */
            #chatbox::-webkit-scrollbar {
                width: 6px;
            }

            #chatbox::-webkit-scrollbar-track {
                background: #f1f1f1;
            }

            #chatbox::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 3px;
            }

            #chatbox::-webkit-scrollbar-thumb:hover {
                background: #555;
            }

            /* --- Responsive --- */
            @media (max-width: 500px){
                .chat-container { width: 95%; }
            }

        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">Customer Support</div>
            <div id="chatbox"></div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Type a message..." onkeydown="if(event.key==='Enter'){sendMessage();}" />
                <button id="sendBtn" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            function sendMessage() {
                const inputBox = document.getElementById("userInput");
                const message = inputBox.value;
                if(message.trim() === "") return;

                addMessage(message, "user-msg");

                fetch("/get_response", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, "bot-msg");
                });

                inputBox.value = "";
            }

            function addMessage(message, className) {
                const chatbox = document.getElementById("chatbox");
                const msgDiv = document.createElement("div");
                msgDiv.className = "message " + className;
                msgDiv.innerText = message;
                chatbox.appendChild(msgDiv);
                chatbox.scrollTop = chatbox.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    response = get_bot_response(user_input)
    return jsonify({"response": response})

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
