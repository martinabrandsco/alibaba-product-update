from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Vercel!",
        "status": "working",
        "platform": "vercel"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    })

# This is the entry point for Vercel
if __name__ == '__main__':
    app.run(debug=True)
