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

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    total = len(result)
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_result = result[start:end]

    return jsonify({
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        },
        'results': paginated_result
    })


@app.route('/search/bm25', methods=['GET'])
def search_bm25_route():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    result = search_bm25(query)

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    total = len(result)
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_result = result[start:end]

    return jsonify({
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        },
        'results': paginated_result
    })


if __name__ == '__main__':
    app.run(debug=True)
