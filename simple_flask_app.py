from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        some_json = request.get_json()
        # curl -H "Content-Type: application/json" -X POST
        # -d '{"name":"xyz", "address":"xyz"}' http://127.0.0.1:5000/
        return jsonify({'you sent': some_json}), 201
    else:
        return jsonify({"about": "Hello World!"})


@app.route('/multi/<int:num>', methods=["GET"])
def get_multiply10(num):
    # curl http://127.0.0.1:5000/multi/23
    return jsonify({'result': num * 10})


if __name__ == '__main__':
    app.run(debug=True)