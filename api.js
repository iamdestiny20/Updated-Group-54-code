import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/recommend/";

export const getRecommendations = async (likedCourse) => {
    try {
        console.log("📡 Sending request to:", API_URL);
        console.log("📝 Payload:", { liked_course: likedCourse });

        const csrfToken = getCookie("csrftoken") || ""; // Retrieve CSRF token
        const token = localStorage.getItem("authToken") || ""; // Retrieve auth token
        console.log("🔑 CSRF Token:", csrfToken);
        console.log("🔐 Auth Token:", token);

        const response = await axios.post(
            API_URL,
            { liked_course: likedCourse },
            {
                withCredentials: true,
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": token ? `Token ${token}` : "", // Fix syntax error
                    "X-CSRFToken": csrfToken, // Send CSRF token
                },
            }
        );

        console.log("✅ Response:", response.data);
        return response.data.recommended_courses;
    } catch (error) {
        console.error("❌ Axios Error:", error);
        if (error.response) {
            console.error("📌 Server Response:", error.response.status, error.response.data);
        } else if (error.request) {
            console.error("📌 No Response from Server:", error.request);
        } else {
            console.error("📌 Request Error:", error.message);
        }
        return [];
    }
};

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
