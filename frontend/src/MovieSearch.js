import React, { useState } from "react";
import axios from "axios";

const MovieSearch = () => {
  const [movieTitle, setMovieTitle] = useState("");
  const [movieData, setMovieData] = useState(null);
  const [error, setError] = useState("");

  const fetchMovie = async () => {
    setError("");
    setMovieData(null);

    try {
        const response = await axios.get("http://127.0.0.1:5000/api/movie", {
            params: { title: movieTitle },
        });
        console.log("API Response:", response.data); // Debug log
        setMovieData(response.data);
    } catch (err) {
        console.error("Error fetching data:", err); // Debug log
        setError(err.response?.data?.error || "Error fetching movie details.");
    }
};


  return (
    <div>
      <input
        type="text"
        placeholder="Enter movie title"
        value={movieTitle}
        onChange={(e) => setMovieTitle(e.target.value)}
      />
      <button onClick={fetchMovie}>Search</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {movieData && (
        <div>
          <h2>{movieData.Title}</h2>
          <p><strong>Year:</strong> {movieData.Year}</p>
          <p><strong>Genre:</strong> {movieData.Genre}</p>
          <p><strong>Director:</strong> {movieData.Director}</p>
          <p><strong>Actors:</strong> {movieData.Actors}</p>
          <p><strong>Plot:</strong> {movieData.Plot}</p>
          <p><strong>IMDb Rating:</strong> {movieData.imdbRating}</p>
        </div>
      )}
    </div>
  );
};

export default MovieSearch;
