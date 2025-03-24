import React, { useState } from "react";
import { getRecommendations } from "./services/api";
import "./App.css"; // Import styles
import Moodlecourses from "./Moodlecourses";



function App() {
  const [userId, setUserId] = useState(""); // State for user input
  const [course, setCourse] = useState(""); // State for course input
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);


  // Function to fetch recommendations
  const fetchRecommendations = async () => {
    if (!userId || !course) {
      alert("Please enter both User ID and Course Name!");
      return;
    }

    setLoading(true);
    const courses = await getRecommendations(userId, course);
    setRecommendations(courses);
    setLoading(false);
  };

  return (
    <div>
      <h1>Welcome to My Moodle Integration</h1>
      <Moodlecourses />
    </div>
  );

  return (
    <div className="container">
      <h1>📚 Course Recommender</h1>

      {/* User ID Input */}
      <input
        type="text"
        placeholder="Enter User ID..."
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="input-field"
      />

      {/* Course Name Input */}
      <input
        type="text"
        placeholder="Enter Course Name..."
        value={course}
        onChange={(e) => setCourse(e.target.value)}
        className="input-field"
      />

      {/* Get Recommendations Button */}
      <button onClick={fetchRecommendations} disabled={loading}>
        {loading ? "Loading..." : "Get Recommendations"}
      </button>

      {/* Display Recommendations */}
      <h2>Recommended Courses:</h2>
      <ul>
        {recommendations.length > 0 ? (
          recommendations.map((rec, index) => <li key={index}>{rec}</li>)
        ) : (
          <p>No recommendations yet.</p>
        )}
      </ul>
    </div>
  );
}

export default App;
