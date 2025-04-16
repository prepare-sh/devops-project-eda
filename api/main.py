# app.py
from flask import Flask, jsonify, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock data for development - Updated movie categories
mock_categories = [
    {
        "id": "trending",
        "name": "Trending Now",
        "description": "What everyone's watching right now.",
        "imageUrl": "https://st.depositphotos.com/1048238/2171/i/450/depositphotos_21718361-stock-photo-trending-concept.jpg"
    },
    {
        "id": "movies",
        "name": "Movies",
        "description": "Our collection of feature films.",
        "imageUrl": "https://img.freepik.com/premium-vector/popcorn-box-icon-pop-corn-icon-symbol-food-cinema-movie-film-isolated-blue-background_654297-709.jpg"
    },
    {
        "id": "tvshows",
        "name": "TV Shows",
        "description": "The best series to binge watch.",
        "imageUrl": "https://c8.alamy.com/comp/KC17YK/popcorn-icon-symbol-food-cinema-movie-film-flat-vector-stock-bowl-KC17YK.jpgg"
    },
    {
        "id": "new",
        "name": "New Releases",
        "description": "Recently added to our library.",
        "imageUrl": "https://media.istockphoto.com/id/467593801/vector/popcorn-falling-in-the-stiped-bag-illustration.jpg?s=612x612&w=is&k=20&c=-w7kmcXSeVk3GR7ltm7gql1E92bSUQOwqETH92L1uVY="
    },
    {
        "id": "mylist",
        "name": "My List",
        "description": "Your saved content for later.",
        "imageUrl": "https://cdn.shopify.com/s/files/1/0558/6413/1764/files/10_Top_Illustration_Styles_That_is_Popular_in_2024_9_1024x1024.jpg?v=1712248143"
    },
    {
        "id": "action",
        "name": "Action",
        "description": "High-octane thrills and adventure.",
        "imageUrl": "https://cdn.prod.website-files.com/60f85e33b5a89c61fcd8377d/672c2576b681985f6d8ace9a_Screen_Shot_2022-07-18_at_2.10.40_PM.png"
    }
]

mock_movies = [
    {
        "id": "1",
        "name": "Inception",
        "director": "Christopher Nolan",
        "rating": 8.8,
        "categoryId": "movies",
        "category": "Movies",
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "imageUrl": "https://upload.wikimedia.org/wikipedia/fi/thumb/1/17/Inception-poster.jpg/250px-Inception-poster.jpg",
        "duration": 148,
        "released": 2010,
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page"
    },
    {
        "id": "2",
        "name": "The Dark Knight",
        "director": "Christopher Nolan",
        "rating": 9.0,
        "categoryId": "movies",
        "category": "Movies",
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "imageUrl": "https://filmartgallery.com/cdn/shop/products/DarkKnight_27x40_original_film_art_5000x.jpg",
        "duration": 152,
        "released": 2008,
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart"
    },
    {
        "id": "3",
        "name": "Stranger Things",
        "director": "The Duffer Brothers",
        "rating": 8.7,
        "categoryId": "tvshows",
        "category": "TV Shows",
        "description": "When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.",
        "imageUrl": "https://upload.wikimedia.org/wikipedia/en/7/78/Stranger_Things_season_4.jpg",
        "duration": 50,
        "released": 2016,
        "cast": "Millie Bobby Brown, Finn Wolfhard, Winona Ryder"
    },
    {
        "id": "4",
        "name": "Breaking Bad",
        "director": "Vince Gilligan",
        "rating": 9.5,
        "categoryId": "tvshows",
        "category": "TV Shows",
        "description": "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family's future.",
        "imageUrl": "https://images.justwatch.com/poster/306097794/s718/breaking-bad.jpg",
        "duration": 49,
        "released": 2008,
        "cast": "Bryan Cranston, Aaron Paul, Anna Gunn"
    },
    {
        "id": "5",
        "name": "Interstellar",
        "director": "Christopher Nolan",
        "rating": 8.6,
        "categoryId": "movies",
        "category": "Movies",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "imageUrl": "https://m.media-amazon.com/images/I/81s+z5z+KUL._AC_SL1500_.jpg",
        "duration": 169,
        "released": 2014,
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain"
    },
    {
        "id": "6",
        "name": "The Queen's Gambit",
        "director": "Scott Frank",
        "rating": 8.6,
        "categoryId": "tvshows",
        "category": "TV Shows",
        "description": "Orphaned at the tender age of nine, prodigious introvert Beth Harmon discovers and masters the game of chess in 1960s USA. But child stardom comes at a price.",
        "imageUrl": "https://m.media-amazon.com/images/I/81s+z5z+KUL._AC_SL1500_.jpg",
        "duration": 60,
        "released": 2020,
        "cast": "Anya Taylor-Joy, Chloe Pirrie, Bill Camp"
    },
    {
        "id": "7",
        "name": "Dune",
        "director": "Denis Villeneuve",
        "rating": 8.1,
        "categoryId": "new",
        "category": "New Releases",
        "description": "Feature adaptation of Frank Herbert's science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and most vital element in the galaxy.",
        "imageUrl": "https://upload.wikimedia.org/wikipedia/en/8/8e/Dune_%282021_film%29.jpg",
        "duration": 155,
        "released": 2021,
        "cast": "Timothée Chalamet, Rebecca Ferguson, Zendaya"
    },
    {
        "id": "8", 
        "name": "The Witcher", 
        "director": "Lauren Schmidt Hissrich",
        "rating": 8.2, 
        "categoryId": "tvshows",
        "category": "TV Shows",
        "description": "Geralt of Rivia, a solitary monster hunter, struggles to find his place in a world where people often prove more wicked than beasts.",
        "imageUrl": "/images/movies/witcher.jpg",
        "duration": 60,
        "released": 2019,
        "cast": "Henry Cavill, Freya Allan, Anya Chalotra"
    },
    {
        "id": "9", 
        "name": "The Matrix", 
        "director": "The Wachowskis",
        "rating": 8.7, 
        "categoryId": "action",
        "category": "Action",
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "imageUrl": "/images/movies/matrix.jpg",
        "duration": 136,
        "released": 1999,
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss"
    },
    {
        "id": "10", 
        "name": "John Wick", 
        "director": "Chad Stahelski",
        "rating": 7.4, 
        "categoryId": "action",
        "category": "Action",
        "description": "An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.",
        "imageUrl": "/images/movies/john-wick.jpg",
        "duration": 101,
        "released": 2014,
        "cast": "Keanu Reeves, Michael Nyqvist, Alfie Allen"
    },
    {
        "id": "11", 
        "name": "Squid Game", 
        "director": "Hwang Dong-hyuk",
        "rating": 8.0, 
        "categoryId": "trending",
        "category": "Trending Now",
        "description": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games. Inside, a tempting prize awaits with deadly high stakes.",
        "imageUrl": "https://static1.srcdn.com/wordpress/wp-content/uploads/2025/01/characters-from-squid-game-unleashed.jpg",
        "duration": 55,
        "released": 2021,
        "cast": "Lee Jung-jae, Park Hae-soo, Wi Ha-jun"
    },
    {
        "id": "12", 
        "name": "No Time to Die", 
        "director": "Cary Joji Fukunaga",
        "rating": 7.3, 
        "categoryId": "new",
        "category": "New Releases",
        "description": "James Bond has left active service. His peace is short-lived when Felix Leiter, an old friend from the CIA, turns up asking for help.",
        "imageUrl": "/images/movies/no-time-to-die.jpg",
        "duration": 163,
        "released": 2021,
        "cast": "Daniel Craig, Ana de Armas, Rami Malek"
    },
    {
        "id": "13", 
        "name": "The Mandalorian", 
        "director": "Jon Favreau",
        "rating": 8.7, 
        "categoryId": "trending",
        "category": "Trending Now",
        "description": "The travels of a lone bounty hunter in the outer reaches of the galaxy, far from the authority of the New Republic.",
        "imageUrl": "https://www.komar.de/media/catalog/product/cache/5/image/9df78eab33525d08d6e5fb8d27136e95/d/x/dx4-086_star_wars_the_mandalorian_the_hunter_web.jpg",
        "duration": 40,
        "released": 2019,
        "cast": "Pedro Pascal, Carl Weathers, Giancarlo Esposito"
    },
    {
        "id": "14", 
        "name": "Shang-Chi", 
        "director": "Destin Daniel Cretton",
        "rating": 7.4, 
        "categoryId": "new",
        "category": "New Releases",
        "description": "Shang-Chi, the master of weaponry-based Kung Fu, is forced to confront his past after being drawn into the Ten Rings organization.",
        "imageUrl": "/images/movies/shang-chi.jpg",
        "duration": 132,
        "released": 2021,
        "cast": "Simu Liu, Awkwafina, Tony Leung Chiu-wai"
    }
]

# Mock watchlist data
mock_watchlist = []

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(mock_categories)

@app.route('/api/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    category = next((c for c in mock_categories if c['id'] == category_id), None)
    if category:
        return jsonify(category)
    return jsonify({"error": "Category not found"}), 404

@app.route('/api/categories/<category_id>/movies', methods=['GET'])
def get_movies_by_category(category_id):
    movies = [m for m in mock_movies if m['categoryId'] == category_id]
    return jsonify(movies)

@app.route('/api/movies/featured', methods=['GET'])
def get_featured_movies():
    # Return a subset of movies as featured
    featured_ids = ["1", "3", "7", "11", "13"]
    featured = [m for m in mock_movies if m['id'] in featured_ids]
    return jsonify(featured)

@app.route('/api/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = next((m for m in mock_movies if m['id'] == movie_id), None)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    return jsonify(mock_watchlist)

@app.route('/api/watchlist/add', methods=['POST'])
def add_to_watchlist():
    data = request.json
    movie_id = data.get('movieId')
    
    movie = next((m for m in mock_movies if m['id'] == movie_id), None)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    
    # Check if the movie is already in the watchlist
    watchlist_item = next((item for item in mock_watchlist if item['id'] == movie_id), None)
    if watchlist_item:
        return jsonify({"success": True, "message": "Movie already in your watchlist"})
    else:
        mock_watchlist.append({
            "id": movie_id,
            "name": movie['name'],
            "director": movie['director'],
            "rating": movie['rating'],
            "duration": movie['duration'],
            "imageUrl": movie['imageUrl']
        })
    
    return jsonify({"success": True})

@app.route('/api/watchlist/remove/<item_id>', methods=['DELETE'])
def remove_from_watchlist(item_id):
    global mock_watchlist
    mock_watchlist = [item for item in mock_watchlist if item['id'] != item_id]
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)