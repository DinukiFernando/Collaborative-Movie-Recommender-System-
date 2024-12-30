// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import "./App.css";

// const App = () => {
//   const [movieTitle, setMovieTitle] = useState("");
//   const [suggestions, setSuggestions] = useState([]);
//   const [movieNames, setMovieNames] = useState([]);
//   const [userId, setUserId] = useState("");
//   const [recommendations, setRecommendations] = useState([]);
//   const [recommendationType, setRecommendationType] = useState("hybrid");
//   const [error, setError] = useState("");

//   useEffect(() => {
//     // Fetch all movie names for autocomplete
//     const fetchMovieNames = async () => {
//       try {
//         const response = await axios.get("http://127.0.0.1:5000/api/movies");
//         setMovieNames(response.data || []);
//       } catch (err) {
//         console.error("Error fetching movie names:", err);
//       }
//     };
//     fetchMovieNames();
//   }, []);

//   const handleInputChange = (value) => {
//     setMovieTitle(value);
//     if (value.length > 0) {
//       const filteredSuggestions = movieNames.filter((name) =>
//         name.toLowerCase().startsWith(value.toLowerCase())
//       );
//       setSuggestions(filteredSuggestions.slice(0, 5)); // Limit to top 5 suggestions
//     } else {
//       setSuggestions([]);
//     }
//   };

//   const handleSuggestionClick = (suggestion) => {
//     setMovieTitle(suggestion);
//     setSuggestions([]);
//   };

//   const fetchRecommendations = async () => {
//     setError("");
//     setRecommendations([]);

//     try {
//       let endpoint = "";
//       if (recommendationType === "content") {
//         endpoint = "http://127.0.0.1:5000/api/content";
//       } else if (recommendationType === "collaborative") {
//         endpoint = "http://127.0.0.1:5000/api/collaborative";
//       } else {
//         endpoint = "http://127.0.0.1:5000/api/hybrid";
//       }

//       const response = await axios.get(endpoint, {
//         params: { title: movieTitle, user_id: userId },
//       });

//       setRecommendations(response.data.recommendations || []);
//     } catch (err) {
//       console.error(err);
//       setError(err.response?.data?.error || "Error fetching recommendations.");
//     }
//   };

//   return (
//     <div className="app">
//       <header className="header">
//         <h1>🎬 Netflix-Inspired Movie Recommendations</h1>
//       </header>

//       <div className="search-section">
//         <div className="search-card">
//           <div className="input-group">
//             <label>Recommendation Type:</label>
//             <select
//               className="form-control"
//               value={recommendationType}
//               onChange={(e) => setRecommendationType(e.target.value)}
//             >
//               <option value="hybrid">Hybrid</option>
//               <option value="content">Content-Based</option>
//               <option value="collaborative">Collaborative</option>
//             </select>
//           </div>

//           <div className="input-group">
//             <label>Movie Title:</label>
//             <input
//               type="text"
//               placeholder="Enter movie title (e.g., Toy Story (1995))"
//               value={movieTitle}
//               onChange={(e) => handleInputChange(e.target.value)}
//             />
//             {/* Autocomplete Dropdown */}
//             {suggestions.length > 0 && (
//               <ul className="suggestions">
//                 {suggestions.map((suggestion, index) => (
//                   <li
//                     key={index}
//                     onClick={() => handleSuggestionClick(suggestion)}
//                   >
//                     {suggestion}
//                   </li>
//                 ))}
//               </ul>
//             )}
//           </div>

//           {recommendationType !== "content" && (
//             <div className="input-group">
//               <label>User ID:</label>
//               <input
//                 type="number"
//                 placeholder="Enter user ID"
//                 value={userId}
//                 onChange={(e) => setUserId(e.target.value)}
//               />
//             </div>
//           )}

//           <button className="btn" onClick={fetchRecommendations}>
//             Get Recommendations
//           </button>
//         </div>
//       </div>

//       {error && <div className="error">{error}</div>}

//       {recommendations.length > 0 && (
//         <div className="recommendations-section">
//           <h2>Recommended Movies</h2>
//           <div className="movie-carousel">
//             {recommendations.map((rec, index) => (
//               <div key={index} className="movie-card">
//                 <img
//                   src={rec.poster}
//                   alt={rec.title}
//                   className="movie-poster"
//                 />
//                 <p className="movie-title">{rec.title}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default App;


import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [movieTitle, setMovieTitle] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [movieNames, setMovieNames] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [recommendationType, setRecommendationType] = useState("hybrid");
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch all movie names for autocomplete
    const fetchMovieNames = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/movies");
        setMovieNames(response.data || []);
      } catch (err) {
        console.error("Error fetching movie names:", err);
      }
    };
    fetchMovieNames();
  }, []);




  const handleInputChange = (value) => {
    setMovieTitle(value);
    if (value.length > 0) {
      const filteredSuggestions = movieNames.filter((name) =>
        name.toLowerCase().startsWith(value.toLowerCase())
      );
      setSuggestions(filteredSuggestions.slice(0, 5)); // Limit to top 5 suggestions
    } else {
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setMovieTitle(suggestion);
    setSuggestions([]);
  };

  const fetchRecommendations = async () => {
    setError("");
    setRecommendations([]);

    try {
      let endpoint = "";
      if (recommendationType === "content") {
        endpoint = "http://127.0.0.1:5000/api/content";
      } else if (recommendationType === "collaborative") {
        endpoint = "http://127.0.0.1:5000/api/collaborative";
      } else {
        endpoint = "http://127.0.0.1:5000/api/hybrid";
      }

      const response = await axios.get(endpoint, {
        params: { title: movieTitle },
      });

      setRecommendations(response.data.recommendations || []);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Error fetching recommendations.");
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🎬 Netflix-Inspired Movie Recommendations</h1>
      </header>

      <div className="search-section">
        <div className="search-card">
          <div className="input-group">
            <label>Recommendation Type:</label>
            <select
              className="form-control"
              value={recommendationType}
              onChange={(e) => setRecommendationType(e.target.value)}
            >
              <option value="hybrid">Hybrid</option>
              <option value="content">Content-Based</option>
              <option value="collaborative">Collaborative</option>
            </select>
          </div>

          <div className="input-group">
            <label>Movie Title:</label>
            <input
              type="text"
              placeholder="Enter movie title (e.g., Toy Story (1995))"
              value={movieTitle}
              onChange={(e) => handleInputChange(e.target.value)}
            />
            {/* Autocomplete Dropdown */}
            {suggestions.length > 0 && (
              <ul className="suggestions">
                {suggestions.map((suggestion, index) => (
                  <li
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    {suggestion}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <button className="btn" onClick={fetchRecommendations}>
            Get Recommendations
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {recommendations.length > 0 && (
        <div className="recommendations-section">
          <h2>Recommended Movies</h2>
          <div className="movie-carousel">
            {recommendations.map((rec, index) => (
              <div key={index} className="movie-card">
                <img
                  src={rec.poster}
                  alt={rec.title}
                  className="movie-poster"
                  onError={(e) =>
                    (e.target.src =
                      "https://via.placeholder.com/300x450?text=No+Image")
                  }
                />
                <p className="movie-title">{rec.title}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
