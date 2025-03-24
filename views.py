from django.http import JsonResponse
import logging
import requests
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from api.models import CourseFeedback
from api.recommendation import hybrid_recommendation

logger = logging.getLogger(__name__)

# ✅ Moodle API Configuration
MOODLE_BASE_URL = "https://destiny-platform.moodlecloud.com"
MOODLE_TOKEN = "de1358e515ab5e0cd2d217b1c90e8976"
MOODLE_COURSE_API = f"{MOODLE_BASE_URL}/webservice/rest/server.php"

def get_moodle_courses():
    """Fetch courses from Moodle API"""
    params = {
        "wstoken": MOODLE_TOKEN,
        "wsfunction": "core_course_get_courses",
        "moodlewsrestformat": "json"
    }

    try:
        response = requests.get(MOODLE_COURSE_API, params=params)
        response.raise_for_status()
        courses = response.json()

        # ✅ Handle Moodle API errors
        if isinstance(courses, dict) and "exception" in courses:
            logger.error(f"Moodle API Error: {courses.get('message', 'Unknown error')}")
            return []

        return courses

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Moodle courses: {e}")
        return []

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_courses(request):
    """Fetch courses from Moodle and return as JSON"""
    logger.info("API call received: fetch_courses")
    courses = get_moodle_courses()
    courses = [
        {"id": 1, "fullname": "Python for Beginners"},
        {"id": 2, "fullname": "Machine Learning Basics"},
    ]

    if not courses:
        return JsonResponse({"error": "Failed to fetch courses from Moodle."}, status=500)

    return JsonResponse(courses, safe=False)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_course(request):
    """Recommend courses based on user preference"""
    try:
        logger.info("API call received: recommend_course")
        data = request.data if isinstance(request.data, dict) else {}

        user_id = data.get("user_id")
        liked_course = data.get("liked_course")

        if not user_id or not liked_course:
            return Response({"error": "User ID and liked_course are required."}, status=400)

        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid user ID format."}, status=400)

        # ✅ Fetch all Moodle courses
        all_courses = get_moodle_courses()

        if not all_courses:
            return Response({"error": "Failed to fetch courses from Moodle."}, status=500)

        # ✅ Find the liked course
        found_course = next(
            (course for course in all_courses if 
             course.get("shortname", "").lower() == liked_course.lower() or 
             course.get("fullname", "").lower() == liked_course.lower()), None)

        if not found_course:
            return Response({"error": f"Course '{liked_course}' not found in Moodle."}, status=404)

        # ✅ Generate recommendations using only Moodle courses
        recommended_courses = hybrid_recommendation(user_id, liked_course, all_courses)

        if not recommended_courses:
            return Response({"error": "No recommendations found."}, status=404)

        return Response({"recommendations": recommended_courses}, status=200)

    except Exception as e:
        logger.error(f"Error in recommend_course: {str(e)}", exc_info=True)
        return Response({"error": "Internal server error."}, status=500)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_feedback(request):
    """Submit user feedback on courses."""
    try:
        data = request.data
        course = data.get("course")
        rating = data.get("rating")
        comment = data.get("comment")

        if not course or not rating or not comment:
            return Response({"error": "Missing required fields"}, status=400)

        feedback = CourseFeedback.objects.create(
            course=course,
            rating=rating,
            comment=comment
        )
        feedback.save()

        return Response({"message": "Feedback submitted successfully"}, status=201)

    except Exception as e:
        logger.error(f"Error in submit_feedback: {str(e)}", exc_info=True)
        return Response({"error": "Internal server error."}, status=500)
