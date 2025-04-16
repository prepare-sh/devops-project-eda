import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function MovieDetail() {
  const { movieId } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    setLoading(true);
    fetch(`/api/movies/${movieId}`)
      .then(res => res.json())
      .then(data => {
        setMovie(data);
        setLoading(false);
      });
  }, [movieId]);

  const addToWatchlist = () => {
    fetch('/api/watchlist/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        movieId: movieId
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Added to your watchlist!');
      } else {
        alert('Error adding to watchlist: ' + (data.error || 'Unknown error'));
      }
    })
    .catch(error => {
      alert('Error: ' + error.message);
    });
  };

  const startStreaming = () => {
    alert(`Now streaming: ${movie.name}`);
    // In a real app, this would initiate the streaming player
  };

  if (loading) {
    return <div className="loading">Loading content...</div>;
  }

  if (!movie) {
    return <div className="not-found">Movie not found</div>;
  }

  return (
    <div className="movie-detail">
      <div className="movie-image">
        <img src={movie.imageUrl} alt={movie.name} />
      </div>
      <div className="movie-details">
        <h1>{movie.name}</h1>
        <h2>Directed by {movie.director}</h2>
        <div className="rating">
          <span className="material-icons">star</span>
          <span>{movie.rating}/10</span>
        </div>
        
        <div className="movie-description">
          <h3>Synopsis</h3>
          <p>{movie.description}</p>
        </div>
        
        <div className="movie-meta">
          <div className="meta-item">
            <span>Genre:</span> 
            <Link to={`/category/${movie.categoryId}`}>{movie.category}</Link>
          </div>
          <div className="meta-item">
            <span>Duration:</span> {movie.duration} min
          </div>
          <div className="meta-item">
            <span>Released:</span> {movie.released}
          </div>
          <div className="meta-item">
            <span>Cast:</span> {movie.cast}
          </div>
        </div>
        
        <div className="watch-options">
          <button onClick={startStreaming} className="watch-now">
            <span className="material-icons">play_arrow</span> Watch Now
          </button>
          <button onClick={addToWatchlist} className="add-to-list">
            <span className="material-icons">playlist_add</span> Add to My List
          </button>
        </div>
      </div>
    </div>
  );
}

export default MovieDetail;