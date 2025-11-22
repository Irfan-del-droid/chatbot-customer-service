from flask import Flask, request, jsonify, render_template

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
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    response = get_bot_response(user_input)
    return jsonify({"response": response})

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
