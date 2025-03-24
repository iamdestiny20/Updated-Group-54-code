import requests
import logging
import pandas as pd
from flask import Flask, request, jsonify
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Moodle API Configuration
MOODLE_BASE_URL = "https://30d1-129-205-124-243.ngrok-free.app"
MOODLE_TOKEN = "de1358e515ab5e0cd2d217b1c90e8976"
MOODLE_COURSE_API = f"{MOODLE_BASE_URL}/webservice/rest/server.php"

# ✅ Flask App
app = Flask(__name__)

# 🔹 Fetch all courses from Moodle
def get_moodle_courses():
    params = {
        "wstoken": MOODLE_TOKEN,
        "wsfunction": "core_course_get_courses",
        "moodlewsrestformat": "json"
    }
    
    try:
        response = requests.get(MOODLE_COURSE_API, params=params)
        response.raise_for_status()
        courses = response.json()

        if isinstance(courses, dict) and "exception" in courses:
            logger.error(f"Moodle API Error: {courses.get('message', 'Unknown error')}")
            return []

        return courses

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Moodle courses: {e}")
        return []

# 🔹 Fetch user enrollments from Moodle
def get_user_courses(user_id):
    params = {
        "wstoken": MOODLE_TOKEN,
        "wsfunction": "core_enrol_get_users_courses",
        "moodlewsrestformat": "json",
        "userid": user_id
    }

    try:
        response = requests.get(MOODLE_COURSE_API, params=params)
        response.raise_for_status()
        courses = response.json()

        if isinstance(courses, dict) and "exception" in courses:
            logger.error(f"Moodle API Error: {courses.get('message', 'Unknown error')}")
            return []

        return courses

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching user courses: {e}")
        return []

# 🔹 Build the User-Course Interaction Matrix
def build_user_course_matrix(user_ids):
    user_course_matrix = defaultdict(lambda: defaultdict(int))

    for user_id in user_ids:
        courses = get_user_courses(user_id)
        for course in courses:
            user_course_matrix[user_id][course["id"]] = 1  # 1 if enrolled

    df = pd.DataFrame(user_course_matrix).fillna(0).T  # Users as rows, courses as columns
    return df

# 🔹 Content-Based Filtering
def content_based_recommendation(liked_course, num_recommendations=5):
    courses = get_moodle_courses()
    
    if not courses:
        return ["No courses available from Moodle"]

    df = pd.DataFrame(courses)
    df["fullname"] = df.get("fullname", "").fillna("Unknown Course")
    df["summary"] = df.get("summary", "").fillna("")
    
    df["combined_features"] = df["fullname"].str.lower().str.strip() + " " + df["summary"].str.lower().str.strip()
    
    liked_course_clean = liked_course.lower().strip()
    found_course = df[df["fullname"].str.lower().str.strip() == liked_course_clean]

    if found_course.empty:
        return [f"Course '{liked_course}' not found in Moodle"]

    idx = found_course.index[0]
    
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["combined_features"])
    
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    recommended_courses = [df.iloc[i[0]]["fullname"] for i in sim_scores[1:num_recommendations + 1]]

    return recommended_courses

# 🔹 Collaborative Filtering (User-User Similarity)
def collaborative_filtering(user_id, user_course_matrix, num_recommendations=5):
    if user_id not in user_course_matrix.index:
        return ["User has no course history."]

    user_similarities = cosine_similarity(user_course_matrix)
    user_sim_df = pd.DataFrame(user_similarities, index=user_course_matrix.index, columns=user_course_matrix.index)
    
    similar_users = user_sim_df[user_id].sort_values(ascending=False)[1:6]  # Exclude self

    recommended_courses = set()
    for similar_user in similar_users.index:
        courses_taken = set(user_course_matrix.loc[similar_user][user_course_matrix.loc[similar_user] == 1].index)
        recommended_courses.update(courses_taken)

    return list(recommended_courses)[:num_recommendations]

# 🔹 Hybrid Model (Combining Content-Based & Collaborative)
def hybrid_recommendation(user_id, liked_course, num_recommendations=5):
    user_course_matrix = build_user_course_matrix([user_id])  

    content_recs = content_based_recommendation(liked_course, num_recommendations // 2)
    collab_recs = collaborative_filtering(user_id, user_course_matrix, num_recommendations // 2)

    return list(set(content_recs + collab_recs))  

# ✅ API Endpoint for Course Recommendations
@app.route("/api/recommend/", methods=["GET"])
def recommend():
    user_id = request.args.get("user_id")
    liked_course = request.args.get("liked_course")
    
    if not user_id or not liked_course:
        return jsonify({"error": "Missing user_id or liked_course"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user_id"}), 400

    recommendations = hybrid_recommendation(user_id, liked_course)
    
    return jsonify({"recommended_courses": recommendations})

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
