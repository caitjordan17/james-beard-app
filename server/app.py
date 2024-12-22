from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/awards')
def awards():
    return jsonify([{
        "name": "Mona Tongdee",
        "restaurant": "Pusadee's Garden",
        "location": "Pittsburgh, Pennsylvania",
        "category": "Restaurant & Chef",
        "level": "Semifinalist",
        "year": "2024",
        "id": 1
    }])


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5555)
