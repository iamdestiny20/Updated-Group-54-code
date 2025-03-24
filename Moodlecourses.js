import React, { useEffect, useState } from "react";

const MoodleCourses = () => {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetch(" https://30d1-129-205-124-243.ngrok-free.app/api/recommend/") // Change to your Django API URL
      .then((response) => response.json())
      .then((data) => setCourses(data))
      .catch((error) => console.error("Error fetching courses:", error));
  }, []);

  return (
    <div>
      <h2>Moodle Courses</h2>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>{course.fullname}</li>
        ))}
      </ul>
    </div>
  );
  console.log("Fetched courses:", courses);

};

export default MoodleCourses;
