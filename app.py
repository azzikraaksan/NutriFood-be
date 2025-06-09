from flask import Flask, request, jsonify
from search_engine import search_cosine, search_bm25
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/search/cosine', methods=['GET'])
def search_cosine_route():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    result = search_cosine(query)
    return jsonify(result)

@app.route('/search/bm25', methods=['GET'])
def search_bm25_route():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    result = search_bm25(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
