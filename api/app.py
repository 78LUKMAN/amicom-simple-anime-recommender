from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# path model& file sparse
MODEL_PATH = 'anime_recommender_model.pkl'
TFIDF_MATRIX_PATH = 'tfidf_matrix.npz'

# model
model_data = joblib.load(MODEL_PATH)
tfidf_vectorizer = model_data['tfidf_vectorizer']
tfidf_matrix = load_npz(model_data['tfidf_matrix_path'])
dataframe = model_data['dataframe']

@app.route('/anime/recommend', methods=['GET'])
def recommend_anime():
    """Endpoint untuk merekomendasikan anime berdasarkan nama."""
    # Ambil parameter dari query string
    name = request.args.get('name', '').lower()
    top_n = int(request.args.get('top_n', 20))

    if not name:
        return jsonify({"error": "Parameter 'name' harus disediakan."}), 400

    # Cari anime dengan substring
    matching_anime = dataframe[dataframe['name'].str.contains(name, case=False)]

    if matching_anime.empty:
        return jsonify({"error": f"Anime dengan nama mengandung '{name}' tidak ditemukan."}), 404

    # Pilih anime pertama dari hasil pencarian
    idx = matching_anime.index[0]
    selected_anime_name = matching_anime.iloc[0]['name']

    # hitung skor kesamaan
    sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    # urutkan berdasarkan skor kesamaan
    sim_indices = sim_scores.argsort()[-top_n-1:-1][::-1]

    #  rekomendasi
    recommendations = dataframe.iloc[sim_indices][['mal_id', 'name', 'type', 'source', 'image', 'synopsis']]

    response = {
        "query": {
            "name": name,
            "matched_anime": selected_anime_name
        },
        "recommendations": recommendations.to_dict(orient='records')
    }

    return jsonify(response)

@app.route('/anime/filter', methods=['GET'])
def filter_anime():
    """Endpoint untuk mencari anime berdasarkan genre, type, atau source, dengan pagination."""
    genre = request.args.get('genre', '').lower()
    anime_type = request.args.get('type', '').lower()
    source = request.args.get('source', '').lower()
    page = int(request.args.get('page', 1))  # Default page 1
    limit = int(request.args.get('limit', 10))  # Default limit 10

    filtered_df = dataframe

    # filter berdasarkan genre
    if genre:
        filtered_df = filtered_df[filtered_df['genre'].str.contains(genre, case=False, na=False)]

    # filter berdasarkan type
    if anime_type:
        filtered_df = filtered_df[filtered_df['type'].str.contains(anime_type, case=False, na=False)]

    # filter berdasarkan source
    if source and source != 'all':  # Tambahkan pengecekan untuk 'all'
        filtered_df = filtered_df[filtered_df['source'].str.contains(source, case=False, na=False)]
    # Jika source='all', tidak perlu melakukan filtering berdasarkan source

    if filtered_df.empty:
        return jsonify({"error": "Tidak ada anime yang cocok dengan filter yang diberikan."}), 404

    # REPLACE NaN dengan nilai default
    filtered_df = filtered_df.fillna({
        'genre': 'Unknown',
        'image': '',
        'synopsis': 'No synopsis',
        'name': 'Unknown Anime'
    })

    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_df = filtered_df.iloc[start_idx:end_idx]

    # response JSON
    response = {
        "query": {
            "genre": genre,
            "type": anime_type,
            "source": source,
            "page": page,
            "limit": limit,
            "total_results": len(filtered_df)
        },
        "results": paginated_df[['mal_id', 'name', 'type', 'source', 'genre', 'image', 'synopsis']].to_dict(orient='records')
    }

    return jsonify(response)

@app.route('/anime/detail', methods=['GET'])
def detail_anime():
    """Endpoint untuk mendapatkan detail anime berdasarkan `mal_id`."""
    mal_id = request.args.get('mal_id', '').strip()

    # validasi mal_id
    if not mal_id.isdigit():
        return jsonify({"error": "Parameter 'mal_id' harus berupa angka yang valid."}), 400

    mal_id = int(mal_id)

    # cari anime berdasarkan mal_id
    anime = dataframe[dataframe['mal_id'] == mal_id]

    if anime.empty:
        return jsonify({"error": f"Anime dengan mal_id={mal_id} tidak ditemukan."}), 404

    # respons JSON
    anime_detail = anime.fillna({
        'genre': 'Unknown',
        'image': '',
        'synopsis': 'No synopsis available',
        'name': 'Unknown Anime'
    }).to_dict(orient='records')

    return jsonify(anime_detail)

if __name__ == '__main__':
    app.run(debug=True)